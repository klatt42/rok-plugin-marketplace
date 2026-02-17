# Create Business Directory

Automate niche business directory creation: interview -> discover -> enrich -> verify -> export. Produces CSV/Excel/PDF/HTML ready for DirectoryGenius import or standalone use.

## Usage

```
/directory-creator:create-directory                                    # Full interview flow
/directory-creator:create-directory "coffee shops" --geography="Portland, OR"  # Skip niche question
/directory-creator:create-directory --niche="HVAC" --geography="Austin metro" --depth=quick
/directory-creator:create-directory "attorneys" --depth=deep --geography="Maryland"
```

## Arguments

- **niche** (positional or `--niche=`): Business type/category (e.g., "HVAC contractors", "coffee shops", "personal injury attorneys")
- **--geography=** (optional): Geographic scope (city, metro, state, or "national")
- **--depth=** (optional): `quick` (8-12 searches, ~10 min), `standard` (default, 2 agents, ~20 min), `deep` (3 agents + verification, ~40 min)
- **--name=** (optional): Directory name. Auto-generated if skipped.

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Interview

Parse $ARGUMENTS for any pre-filled values (`--niche=`, `--geography=`, `--depth=`, `--name=`). For any values NOT provided via arguments, ask the user using AskUserQuestion. Ask only the questions that are needed (skip any already answered by arguments).

**Questions** (ask only unanswered ones, batch into 1-2 AskUserQuestion calls):

1. **Niche type**: What type of businesses?
   - Options: Restaurants, HVAC/Plumbing, Attorneys/Legal, Medical/Dental, Home Services, Auto Services
   - User can provide custom text

2. **Geographic scope**: What area should the directory cover?
   - Options: Single city (e.g., "Austin, TX"), Metro area (e.g., "Austin metro"), State (e.g., "Texas"), Multi-state / National
   - User provides specific location text

3. **Subcategories** (optional): Any specializations to focus on?
   - Options: Auto-detect from niche (Recommended), Specify manually, Skip subcategories
   - If auto-detect: determine subcategories based on the niche (e.g., HVAC -> residential, commercial, installation, repair)

4. **Target listing count**: How many businesses to find?
   - Options: 25-50 (focused, quick), 100-200 (comprehensive), 500+ (exhaustive, deep only)

5. **Enrichment depth**: How thorough should data collection be?
   - Options: Quick (~10 min, WebSearch only, no agents), Standard (~20 min, search + website enrichment) (Recommended), Deep (~40 min, full enrichment + cross-verification)

6. **Directory name** (optional): What should the directory be called?
   - Options: Auto-generate (Recommended), Custom name
   - Auto-generate format: "[Geography] [Niche] Directory" (e.g., "Austin HVAC Pros")

### Phase 2: Discovery Brief

After collecting all parameters, compile a Discovery Brief:

```
DISCOVERY BRIEF
===============
Directory: [name or auto-generated]
Niche: [niche type]
Geography: [location] ([city/metro/state/national])
Subcategories: [list or "auto-detect"]
Target count: [25-50 / 100-200 / 500+]
Depth: [quick / standard / deep]
Estimated time: [~10 min / ~20 min / ~40 min]

Search Strategy:
- Primary sources: Yelp, Google Maps, YellowPages, BBB
- Industry sources: [niche-specific directories]
- Enrichment: [None / Website crawling / Full verification]
```

**APPROVAL GATE**: Present the Discovery Brief and ask the user to confirm or adjust before proceeding. Wait for explicit approval.

### Phase 3: Discovery & Enrichment

Dispatch depends on depth level:

#### Quick Mode (no agents)
Perform 8-12 WebSearch queries directly in main context:
1. `"[niche]" "[city/state]" site:yelp.com`
2. `"[niche]" "[city/state]" site:yellowpages.com`
3. `"[niche]" near "[city/state]" reviews OR directory`
4. `"best [niche]" "[city/state]" 2025 OR 2026`
5. `"[niche]" "[city/state]" site:bbb.org`
6. `"[subcategory]" "[city/state]" [niche]` (for each subcategory)
7. `"top [niche]" "[city/state]" list OR directory`
8. `"[niche]" "[city/state]" site:angi.com OR site:homeadvisor.com` (if applicable)

For each search result, extract: business name, address, phone, website URL, rating, review count.
Store results in a running list. Deduplicate by business name (fuzzy 85% match) + phone (exact).

After searches, quality-score each listing:
- Has name + address + phone: base 40 points
- Has website: +15
- Has rating >= 4.0: +15
- Has 10+ reviews: +10
- Has hours/description: +10
- Source from aggregator (Yelp, Google): +10

Assign status: verified (score >= 50), needs_verification (30-49), removed (< 30).

Skip to Phase 5 (Export).

#### Standard Mode (2 parallel agents)
Read agent definitions and launch 2 agents simultaneously in a SINGLE message using `Task` with `run_in_background: true`:

| Agent | File | Subagent Type | Model | Purpose |
|-------|------|--------------|-------|---------|
| business-searcher | `agents/business-searcher.md` | general-purpose | sonnet | 12-18 WebSearch queries across aggregators |
| data-enricher | `agents/data-enricher.md` | general-purpose | sonnet | WebFetch business websites for details |

**For each agent prompt, include**:
1. The agent's full instructions (read from `agents/[agent-name].md` relative to this command)
2. The niche, geography, subcategories, and target count
3. For data-enricher: also pass the initial search results from business-searcher (wait for business-searcher first, or pass the niche details and let enricher search independently)

**Agent dispatch strategy for Standard**:
- Launch business-searcher first (it needs to find businesses)
- Once business-searcher completes, pass its results to data-enricher
- OR: Launch both in parallel — business-searcher finds businesses, data-enricher independently searches for and enriches the top businesses found via its own WebSearch queries

Collect results with `TaskOutput` (block=true). Merge business-searcher discoveries with data-enricher details. Deduplicate by name (85% fuzzy) + phone (exact match).

Proceed to Phase 4.

#### Deep Mode (3 agents, sequential)
Same as Standard, plus a verification step:

1. Launch business-searcher (sonnet) — 20-30 searches
2. Launch data-enricher (sonnet) — enriches all discoveries (not just top 50%)
3. After both complete, launch data-verifier (opus):
   - Read agent definition from `agents/data-verifier.md`
   - Pass ALL merged results
   - Verifier does cross-reference, dedup, quality adjustment

Collect verifier results with `TaskOutput` (block=true).

### Phase 4: Verification & Scoring

After agent results are collected (Standard/Deep), perform final merge:

1. **Deduplicate**: Match by business name (85% similarity) + exact phone match. Keep the record with more data fields populated.
2. **Quality score** each listing (0-100):
   - Name + address + phone present: 30 pts
   - Website URL present: 10 pts
   - Description present (>20 chars): 10 pts
   - Rating present (from any source): 10 pts
   - 10+ reviews: 5 pts
   - Hours present: 5 pts
   - Services/amenities listed: 10 pts
   - Email present: 5 pts
   - Cross-validated by multiple sources: +10 pts (deep mode only)
   - Social links present: 5 pts
3. **Status assignment**:
   - `verified`: score >= 50
   - `needs_verification`: score 30-49
   - `removed`: score < 30 (exclude from exports, but keep in JSON for reference)
4. **Generate slugs**: lowercase name, replace spaces/special chars with hyphens

### Phase 5: Export

1. **Write JSON** to `/tmp/directory_data.json` using the schema defined below.

2. **Run export script**:
```bash
~/.claude/scripts/.venv/bin/python3 [this_plugin_dir]/scripts/directory_export.py --input /tmp/directory_data.json
```

The script generates 4 files to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Directory_Creator/`
- **CSV**: DirectoryGenius-compatible import (matches `businesses` table schema)
- **Excel**: Multi-sheet workbook (Listings, Statistics, Categories, Geography)
- **PDF**: Professional summary report with stats + sample listings
- **HTML**: Styled directory preview with filterable table

3. **Present summary** in chat:

```
## Directory Created: [Directory Name]

**Niche**: [niche] | **Geography**: [geography] | **Depth**: [depth]
**Generated**: [date]

### Statistics
| Metric | Count |
|--------|-------|
| Total found | [N] |
| Verified | [N] |
| Needs verification | [N] |
| Duplicates removed | [N] |
| Low quality removed | [N] |

### Top 5 Listings
| # | Business | City | Score | Rating | Reviews |
|---|----------|------|-------|--------|---------|
| 1 | [name] | [city] | 92 | 4.8 | 156 |
| ... |

### Export Files
- CSV: [path] (DirectoryGenius import ready)
- Excel: [path]
- PDF: [path]
- HTML: [path]

### Next Steps
- `/directory-creator:directory-status` — View/filter all listings
- `/directory-creator:generate-landing-content` — Generate SEO landing page content
- Re-run with `--depth=deep` for cross-verified results
```

## JSON Export Schema

The JSON written to `/tmp/directory_data.json` must follow this structure:

```json
{
  "type": "directory_data",
  "generated_date": "YYYY-MM-DD",
  "directory_name": "Austin HVAC Pros",
  "niche_type": "HVAC contractors",
  "geography": "Austin metro",
  "geography_type": "metro",
  "subcategories": ["residential", "commercial"],
  "depth": "standard",
  "methodology": {
    "agents_dispatched": 2,
    "total_searches": 18,
    "websites_crawled": 45,
    "duration_minutes": 22
  },
  "statistics": {
    "total_found": 120,
    "verified": 85,
    "needs_verification": 15,
    "duplicates_removed": 12,
    "low_quality_removed": 8
  },
  "businesses": [
    {
      "name": "Business Name",
      "slug": "business-name",
      "category": "Subcategory",
      "description": "Description text...",
      "address": "123 Main St",
      "city": "Austin",
      "state": "TX",
      "zip_code": "78701",
      "phone": "+15125551234",
      "email": "info@example.com",
      "website": "https://example.com",
      "hours": "Mon-Fri 8am-6pm",
      "service_radius": 25,
      "rating": 4.8,
      "review_count": 156,
      "services": ["service1", "service2"],
      "amenities": ["amenity1", "amenity2"],
      "service_areas": ["City1", "City2"],
      "social_links": {"facebook": "url", "instagram": "url"},
      "quality_score": 92,
      "status": "verified",
      "source": "yelp.com + website enrichment"
    }
  ]
}
```

## Rules

- This is a READ + EXPORT tool. Never create apps, modify repositories, or write code beyond the JSON/export.
- All business discovery uses WebSearch. Do not fabricate business names, addresses, phone numbers, or reviews.
- Present the Discovery Brief and wait for approval before dispatching agents.
- Handle agent failures gracefully — proceed with available results and note failures in the summary.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Directory_Creator/`
- Quality scoring must be consistent — same business should get same score regardless of depth mode.
- Phone numbers should be normalized to E.164 format (+1XXXXXXXXXX) when possible.
- Addresses should include city, state, and zip when available.
- The CSV export must match DirectoryGenius `businesses` table columns exactly.
