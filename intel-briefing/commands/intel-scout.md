# /intel-scout - Daily Intelligence Scout

Automated content discovery system. Searches for new content from watched creators, trending topics matching active briefing themes, and articles relevant to active predictions. Generates a recommendation list for manual review and selective ingestion.

## Usage

```
/intel-briefing:intel-scout                      # Run full discovery scan
/intel-briefing:intel-scout --creators-only      # Only search watched creators
/intel-briefing:intel-scout --topics-only        # Only search briefing topics
/intel-briefing:intel-scout review               # Review pending recommendations
/intel-briefing:intel-scout approve <id>         # Approve recommendation for ingestion
/intel-briefing:intel-scout approve all          # Approve all above threshold
/intel-briefing:intel-scout reject <id>          # Reject recommendation
/intel-briefing:intel-scout ingest               # Ingest all approved recommendations
```

### Parameters
- **(no args)** - Execute full scout scan (creators + topics)
- **--creators-only** - Only search watched creators, skip topic search
- **--topics-only** - Only search topics/keywords, skip creator search
- **review** - Display pending recommendations sorted by relevance
- **approve** - Mark recommendation for ingestion (by ID or "all" with threshold)
- **reject** - Reject recommendation (by ID)
- **ingest** - Process all approved recommendations through /intel-ingest

### Output Folder
Scout exports go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Outputs/scout/`

Initial request: $ARGUMENTS

## Execution Steps

### Determine Mode

Parse $ARGUMENTS:
- No args, or contains neither "review" nor "approve" nor "reject" nor "ingest" → Mode: Run
- "review" → Mode: Review
- "approve" → Mode: Approve
- "reject" → Mode: Reject
- "ingest" → Mode: Ingest

Check for flags: --creators-only, --topics-only (only relevant for Run mode).

---

### Mode: Run (Full Discovery Scan)

#### Phase 1: Gather Search Context

1. **Load watched creators** from Supabase. Write Python script to `/tmp/scout_load_creators.py`:

```python
import json, os, subprocess

url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

cmd = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_creators?active=eq.true&order=trust_tier.desc,last_checked.asc',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
print(result.stdout)
```

Parse the response into a creators list.

2. **Load latest briefing context**. Write Python script to `/tmp/scout_load_context.py`:

```python
import json, os, subprocess

url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

# Latest briefing themes
cmd1 = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_briefings?order=version.desc&limit=1&select=consensus_themes,contested_topics,metadata',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]
r1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=15)

# Active predictions
cmd2 = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_predictions?outcome=eq.pending&select=prediction_text,category,subcategory,tags&order=current_confidence.desc&limit=20',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]
r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=15)

# Active alerts
cmd3 = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_alerts?active=eq.true&select=topic,keywords,category',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]
r3 = subprocess.run(cmd3, capture_output=True, text=True, timeout=15)

# Already ingested URLs (for dedup)
cmd4 = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_documents?select=source_url&limit=500',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]
r4 = subprocess.run(cmd4, capture_output=True, text=True, timeout=15)

# Already recommended URLs (for dedup)
cmd5 = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_scout_recommendations?select=content_url&limit=500',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]
r5 = subprocess.run(cmd5, capture_output=True, text=True, timeout=15)

print(json.dumps({
    'briefing': json.loads(r1.stdout) if r1.stdout else [],
    'predictions': json.loads(r2.stdout) if r2.stdout else [],
    'alerts': json.loads(r3.stdout) if r3.stdout else [],
    'existing_urls': json.loads(r4.stdout) if r4.stdout else [],
    'recommended_urls': json.loads(r5.stdout) if r5.stdout else []
}))
```

3. **Extract search keywords** from the context:
   - From consensus_themes: extract key topic names and terms
   - From contested_topics: extract topic names
   - From predictions: extract subcategory values and key nouns from prediction_text
   - From alerts: extract all keywords
   - Deduplicate and rank by frequency (terms appearing in multiple sources rank higher)
   - Keep top 15-20 keywords for topic search queries

4. **Build dedup set**: Combine all existing source_url values from documents and content_url values from recommendations into a set for fast lookup.

5. **Expire old recommendations**: Update any pending recommendations older than 14 days to "expired":

Write Python script to expire old recs:
```python
import json, os, subprocess
from datetime import datetime, timedelta

url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')
cutoff = (datetime.utcnow() - timedelta(days=14)).isoformat()

cmd = [
    'curl', '-s', '-X', 'PATCH',
    f'{url}/rest/v1/rok_intel_scout_recommendations?status=eq.pending&discovered_at=lt.{cutoff}',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps({"status": "expired"})
]
subprocess.run(cmd, capture_output=True, text=True, timeout=15)
```

Display:
```
SCOUT CONTEXT LOADED
====================
Watched Creators: [N] active
Briefing Themes:  [N] consensus + [N] contested
Active Predictions: [N] pending
Active Alerts:    [N]
Search Keywords:  [N] extracted
Existing URLs:    [N] (for dedup)
Expired:          [N] old recommendations
```

#### Phase 2: Creator Content Search (skip if --topics-only)

For each watched creator:

1. **Build search query** based on platform:
   - **YouTube**: `"[creator name]" site:youtube.com` — search for recent videos
   - **Twitter/X**: `"[creator name]" OR "[handle]" site:twitter.com OR site:x.com` — search for threads/posts
   - **Substack**: `"[creator name]" site:substack.com` — search for articles
   - **Blog**: `site:[channel_url domain]` — search creator's own site
   - **Podcast**: `"[creator name]" podcast episode` — search for appearances
   - **Research**: `"[creator name]" paper OR research` — search for papers

   Use the creator's `last_checked` date to focus on recent content. If never checked, search the last 7 days.

2. **Execute WebSearch** for each creator:
   ```
   WebSearch(query: "[constructed query]")
   ```

   Rate limit: Maximum 20 creator searches total per run. If more than 20 active creators, prioritize by:
   - HIGH trust tier first
   - Longest time since last_checked second
   - Skip creators checked within the last 24 hours

3. **Parse and score results** for each search:
   - Extract: title, URL, snippet from search results
   - **Filter out**:
     - URLs already in the dedup set (existing documents + existing recommendations)
     - URLs that are clearly not content (e.g., channel pages, playlists, about pages)
     - Content older than 30 days
   - **Score each result**:
     - Base score: 0.50 (from watched creator)
     - +0.20 if creator.trust_tier == 'HIGH'
     - +0.10 if creator.trust_tier == 'MEDIUM'
     - +0.10 if title or snippet contains any extracted search keywords
     - +0.05 per additional matching keyword (max +0.20 additional)
     - Cap total at 1.00
   - **Determine matching pillars** from creator's domain_expertise:
     - "financial", "economic", "macro" → Financial
     - "geopolitical", "political", "military" → Geopolitical
     - "technology", "ai", "semiconductor" → Technology
     - "labor", "employment", "workforce" → Labor

4. **Store recommendations** in Supabase. For each scored result, write to `rok_intel_scout_recommendations`:

Write a Python script to `/tmp/scout_store_recs.py` that takes a JSON array of recommendations and batch-inserts them:

```python
import json, os, subprocess, sys

recs = json.loads(sys.argv[1])  # Or read from /tmp/scout_recs_batch.json
url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

payload_path = '/tmp/scout_recs_payload.json'
with open(payload_path, 'w') as f:
    f.write(json.dumps(recs))

cmd = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_scout_recommendations',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}',
    '-H', 'Content-Type: application/json',
    '-H', 'Prefer: return=representation',
    '-d', f'@{payload_path}'
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
print(result.stdout)
```

Each recommendation record:
```json
{
  "title": "[title from search result]",
  "creator_id": "[creator uuid or null]",
  "creator_name": "[creator name]",
  "platform": "[creator platform]",
  "content_url": "[URL]",
  "publish_date": "[date if available]",
  "relevance_score": 0.75,
  "matching_pillars": ["Financial", "Technology"],
  "matching_keywords": ["DRAM", "compute", "infrastructure"],
  "from_watched_creator": true,
  "status": "pending",
  "metadata": {"search_query": "[the query used]", "snippet": "[search snippet]"}
}
```

5. **Update creator's last_checked** timestamp for each creator searched.

Display progress per creator:
```
Searching creators: [X]/[total]
  [check] Andrei Jikh (YouTube, HIGH) - 3 new items found
  [check] Matt Berman (YouTube, HIGH) - 1 new item found
  [dash]  Wes Roth (YouTube, MED) - No new content
  [check] Nate Jones (YouTube, MED) - 2 new items found

Creator search complete: [N] new recommendations from [M] creators
```

#### Phase 3: Topic-Based Search (skip if --creators-only)

1. **Build topic queries** from the ranked keywords extracted in Phase 1:
   - Combine related keywords into 2-3 word composite queries
   - Examples: "AI regulation policy", "DRAM shortage 2026", "Bitcoin ETF institutional", "China semiconductor self-sufficiency"
   - Prioritize keywords that appear in BOTH predictions AND briefing themes
   - Build up to 10 queries

2. **Execute WebSearch** for each topic query:
   ```
   WebSearch(query: "[keyword combo] analysis OR report 2026")
   ```

   Rate limit: Maximum 10 topic searches per run.

3. **Parse and score results**:
   - **Filter out**:
     - URLs already in dedup set
     - Social media posts (unless from known creator handle)
     - Content older than 14 days for topic search
   - **Score each result**:
     - Base score: 0.30 (topic discovery)
     - +0.20 if from trusted domain:
       - Financial: wsj.com, ft.com, bloomberg.com, reuters.com, economist.com
       - Technology: arstechnica.com, theverge.com, wired.com, arxiv.org, nature.com
       - Geopolitical: foreignaffairs.com, atlanticcouncil.org, cfr.org, aljazeera.com
       - General: nytimes.com, washingtonpost.com, bbc.com, apnews.com
     - +0.15 if matches a prediction subcategory exactly
     - +0.10 if matches an active alert keyword
     - +0.05 per additional keyword match (max +0.25)
     - Cap total at 1.00
   - **Determine matching pillars** from keyword categories (same mapping as Phase 2)

4. **Store recommendations** (same pattern as Phase 2 but with `from_watched_creator: false` and `creator_name: "Topic Discovery"`).

Display progress:
```
Searching topics: [X]/[total]
  [check] "AI regulation policy 2026" - 4 relevant articles
  [check] "DRAM shortage compute" - 2 relevant articles
  [dash]  "Dollar debasement gold" - No new high-quality results
  [check] "China semiconductor TSMC" - 3 relevant articles

Topic search complete: [N] new recommendations from [M] queries
```

#### Phase 4: Deduplication and Ranking

1. If any URL was found by both creator search and topic search, keep the creator-sourced version (higher base score, better attribution).

2. Load all recommendations stored during this session.

3. Sort by:
   - Primary: relevance_score DESC
   - Secondary: from_watched_creator DESC (creator content first)
   - Tertiary: publish_date DESC (newer first)

#### Phase 5: Generate Recommendation Report

1. Create output directory:
```bash
mkdir -p "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Outputs/scout/"
```

2. Generate JSON export to `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Outputs/scout/scout-YYYY-MM-DD.json`:

```json
{
  "generated_at": "[timestamp]",
  "summary": {
    "total_recommendations": 15,
    "from_watched_creators": 8,
    "from_topic_search": 7,
    "creators_checked": 4,
    "topics_searched": 10,
    "avg_relevance_score": 0.68
  },
  "recommendations": [
    {
      "id": "[uuid]",
      "title": "[title]",
      "creator_name": "[name]",
      "platform": "[platform]",
      "url": "[url]",
      "publish_date": "[date]",
      "relevance_score": 0.85,
      "matching_pillars": ["Financial", "Technology"],
      "matching_keywords": ["DRAM", "compute"],
      "from_watched_creator": true,
      "status": "pending"
    }
  ]
}
```

3. Generate Markdown report to `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Outputs/scout/scout-YYYY-MM-DD.md`:

```markdown
# Intelligence Scout Recommendations
**Generated:** YYYY-MM-DD HH:MM
**Total Items:** [N] | **From Creators:** [n] | **From Topics:** [n]

---

## Recommendations (sorted by relevance)

### 1. [Title] - Score: [XX]%
- **Creator:** [Name] ([Platform]) | **Trust:** [tier]
- **Published:** [Date]
- **Pillars:** [list]
- **Keywords:** [list]
- **URL:** [url]
- **Source:** Watched Creator / Topic Discovery

---

(repeat for each recommendation)

## Summary by Pillar

| Pillar | Items | Avg Score |
|--------|-------|-----------|
| Financial | [n] | [score] |
| Geopolitical | [n] | [score] |
| Technology | [n] | [score] |
| Labor | [n] | [score] |

## Next Steps

- Review: `/intel-briefing:intel-scout review`
- Approve items: `/intel-briefing:intel-scout approve [id]`
- Approve all high-relevance: `/intel-briefing:intel-scout approve all`
- Ingest approved: `/intel-briefing:intel-scout ingest`
```

4. Display session summary in terminal:
```
=========================================
SCOUT SCAN COMPLETE
=========================================
Duration: [seconds]s

DISCOVERED:
  Total Recommendations: [N]
    From Watched Creators: [n]
    From Topic Search:     [n]

  By Pillar:
    Financial:    [n] items
    Geopolitical: [n] items
    Technology:   [n] items
    Labor:        [n] items

TOP 5 RECOMMENDATIONS:
  1. [Title] - [Creator] - [Score]% - [URL]
  2. [Title] - [Creator] - [Score]% - [URL]
  3. [Title] - [Creator] - [Score]% - [URL]
  4. [Title] - [Creator] - [Score]% - [URL]
  5. [Title] - [Creator] - [Score]% - [URL]

EXPORTED:
  JSON: PlugIn-Intel-Outputs/scout/scout-[date].json
  MD:   PlugIn-Intel-Outputs/scout/scout-[date].md

=========================================

NEXT STEPS:
  /intel-briefing:intel-scout review         # Review all pending
  /intel-briefing:intel-scout approve all    # Approve high-relevance items
  /intel-briefing:intel-scout ingest         # Ingest approved items
```

---

### Mode: Review

1. Query pending recommendations from Supabase. Write Python script:

```python
import json, os, subprocess

url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

cmd = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_scout_recommendations?status=eq.pending&order=relevance_score.desc,discovered_at.desc',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
print(result.stdout)
```

2. Display formatted table:
```
PENDING RECOMMENDATIONS
=======================
Total: [N] pending

| # | ID   | Title                          | Creator       | Score | Pillars         | Age   |
|---|------|--------------------------------|---------------|-------|-----------------|-------|
| 1 | a1b2 | "AI Regulation Shifts..."      | Andrei Jikh   |  95%  | Financial, Tech | 2h    |
| 2 | c3d4 | "DRAM Shortage Analysis"       | Topic Search  |  82%  | Financial       | 3h    |
| 3 | e5f6 | "New GPU Architecture..."      | Nate Jones    |  78%  | Technology      | 1d    |
...

COMMANDS:
  /intel-briefing:intel-scout approve a1b2       # Approve specific item
  /intel-briefing:intel-scout approve all        # Approve all above 70%
  /intel-briefing:intel-scout reject c3d4        # Reject item
  /intel-briefing:intel-scout ingest             # Ingest all approved
```

3. If no pending recommendations:
```
No pending recommendations.

Run a scout scan to discover new content:
  /intel-briefing:intel-scout
```

---

### Mode: Approve

1. Parse argument: specific ID (first 4+ chars of UUID) or "all".

2. **If specific ID**:
   - Find the recommendation by ID prefix match
   - Update status to "approved" via Python script
   - Display:
   ```
   APPROVED
   ========
   [Title]
   Creator: [name] | Score: [score]%
   URL: [url]

   Status: pending -> approved

   Run /intel-briefing:intel-scout ingest to process approved items.
   ```

3. **If "all"**:
   - Ask: "Approve all items with score >= 70%? (yes/no/custom threshold)"
   - If custom: "Enter minimum score (0-100):"
   - Batch update all pending items above threshold to "approved"
   - Display:
   ```
   BATCH APPROVED
   ==============
   [N] items approved (score >= [threshold]%)
   [M] items remain pending (below threshold)

   Run /intel-briefing:intel-scout ingest to process them.
   ```

---

### Mode: Reject

1. Parse the recommendation ID (first 4+ chars of UUID).

2. Find the recommendation, update status to "rejected".

3. Display:
```
REJECTED
========
[Title] marked as rejected.
It will not appear in future review lists.
```

---

### Mode: Ingest

1. Query all approved recommendations:

```python
import json, os, subprocess

url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

cmd = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_scout_recommendations?status=eq.approved&order=relevance_score.desc',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
print(result.stdout)
```

2. Display ingestion plan:
```
INGESTION PLAN
==============
Approved items: [N]

  1. [Title] - [URL] ([Creator])
  2. [Title] - [URL] ([Creator])
  ...

This will:
  - Download/fetch each item
  - Extract claims and predictions via document-analyst
  - Validate claims via research-validator
  - Store in Supabase
  - Update creator stats
  - Offer briefing update at the end

Proceed? (yes/no)
```

3. For each approved item, trigger the `/intel-ingest` workflow:
   - If URL is a YouTube video: `/intel-briefing:intel-ingest [url] --skip-briefing`
   - If URL is an article/web page: `/intel-briefing:intel-ingest [url] --skip-briefing`
   - On success: update recommendation status to "ingested"
   - On failure: log error, keep status as "approved" for retry

4. After all items processed:
   - Ask: "Update master briefing with new intelligence? (yes/no)"
   - If yes: trigger `/intel-briefing:intel-briefing refresh`

5. Display summary:
```
=========================================
BATCH INGESTION COMPLETE
=========================================
Processed: [N] of [total]
  Successful: [n]
  Failed:     [n]

Documents Stored: [n]
Total Claims: [N]
Total Predictions: [N]

Creator Updates:
  [Creator]: +[n] documents (now [total])
  ...

Master Briefing: [Updated to v[N] / Skipped]
=========================================

NEXT STEPS:
  /intel-briefing:intel-briefing            # View updated briefing
  /intel-briefing:intel-scout               # Run next scout scan
```

## Important Rules

- **Rate limits**: Maximum 30 WebSearch calls per run (20 creator + 10 topic). Do NOT exceed this.
- **Deduplication**: ALWAYS check both rok_intel_documents.source_url AND rok_intel_scout_recommendations.content_url before storing new recommendations
- **Expiration**: Auto-expire pending recommendations older than 14 days at start of each run
- **Creator priority**: When creator search and topic search find the same URL, keep the creator-sourced version
- **Damage control**: ALL Supabase operations via Python scripts to /tmp (avoid `*.key` pattern in bash)
- **Scoring transparency**: Store the search query and snippet in the metadata field for audit trail
- **Platform-specific queries**: Tailor WebSearch to each platform's URL patterns
- **Trusted domains**: Score boost for authoritative sources (WSJ, FT, Bloomberg, Reuters, arxiv, nature.com, etc.)
- **No auto-ingest**: Scout ONLY recommends. Human must explicitly approve before any content is ingested.
- **Keyword extraction**: Remove stop words, prioritize nouns and proper nouns from predictions/themes
