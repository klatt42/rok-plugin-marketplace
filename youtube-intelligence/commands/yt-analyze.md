# /yt-analyze - Analyze a YouTube Video

Extracts structured intelligence from a YouTube video: bulletized summary, validated claims, technical details, and actionable ROK integration recommendations weighted by creator trust.

## Usage

```
/yt-analyze url:https://youtube.com/watch?v=...
/yt-analyze transcript:/path/to/transcript.txt
/yt-analyze url:https://youtube.com/watch?v=... depth:deep focus:MCP
```

Or simply paste a transcript directly after invoking `/yt-analyze`.

### Parameters
- **url** - YouTube video URL
- **transcript** - Path to local transcript file
- **(pasted text)** - User can paste transcript directly in the message
- **depth** - `quick` (summary only) | `standard` (default, includes validation) | `deep` (extensive external research)
- **focus** - Narrow analysis to a specific topic within the video

## Execution Steps

### Step 1: Obtain Video Content

Determine what the user provided and obtain content using this cascade:

1. **If user pasted transcript text** in the message (long block of text, not a URL or file path):
   - Use the pasted text directly as the transcript
   - Ask the user for the video title and channel name if not provided

2. **If `transcript:` parameter provided**:
   - Read the file with the Read tool
   - Extract any metadata from the file header if present

3. **If `url:` parameter provided**:
   - Use WebFetch on the YouTube URL to get the page content
   - Extract: video title, channel name, publish date, description, duration
   - Attempt transcript extraction:
     a. Check if yt-dlp is available: `which yt-dlp`
     b. If yes: `yt-dlp --write-auto-sub --sub-lang en --skip-download --print-to-file subtitle -o "/tmp/claude-yt-%(id)s" "<url>"` then read the subtitle file
     c. If no yt-dlp, use the WebFetch page content + description as the source material
   - If no transcript can be obtained, inform the user:
     ```
     Could not extract transcript automatically. Options:
     1. Paste the transcript from YouTube (click "..." → Show transcript)
     2. Install yt-dlp: pip install yt-dlp
     3. Save transcript to a file and use: /yt-analyze transcript:<path>
     ```

4. **If nothing provided**, ask:
   ```
   Please provide one of:
   - A YouTube URL: /yt-analyze url:https://youtube.com/watch?v=...
   - A transcript file: /yt-analyze transcript:/path/to/file.txt
   - Or paste the transcript directly
   ```

### Step 2: Identify Creator

Load the creator registry from `~/.claude/youtube-intelligence/creators.json`.

Match the channel name against the registry:
1. Exact match on `name` (case-insensitive)
2. Match on any `aliases` entry (case-insensitive)
3. Partial match (channel name contains creator name or vice versa)

If matched:
- Note the trust tier (HIGH/MEDIUM)
- Note domain expertise
- Display: `TRUSTED CREATOR: [name] (trust: [tier], domain: [domains])`

If not matched:
- Assign STANDARD trust tier
- Note: `Creator: [channel name] (trust: STANDARD - not in trusted registry)`

### Step 3: Dispatch Transcript Analysis

Spawn the **transcript-analyst** subagent using the Task tool:

```
Subagent: transcript-analyst
Input: transcript text + video metadata + creator trust info
Output: Structured JSON with classification, key_points, technical_details, claims, quotes
```

Wait for the subagent to return results.

### Step 4: Validation Research (if depth is standard or deep)

If depth is `quick`, skip to Step 5.

Spawn the **research-validator** subagent using the Task tool:

```
Subagent: research-validator
Input: claims list + technical details + video topic + creator info
Output: Structured JSON with validations, tool_verification, additional_context
```

For `deep` depth, also:
- Search for related content by other trusted creators on the same topic
- Find official documentation for all tools/libraries mentioned
- Search for GitHub repos, starter templates, or reference implementations
- Look for "what changed since" if the video is more than 3 months old

### Step 5: Generate ROK Recommendations

Based on the transcript analysis and validation results, generate actionable recommendations.

Apply the weighting formula from the creator-profiles skill:
```
confidence = creator_trust_weight * validation_score * relevance_score
```

Categorize each recommendation:

**Immediate Actions** (difficulty 1-2, can do now):
- Provide specific instructions for what to change and where in ROK

**Requires Planning** (difficulty 3-4, needs /2_plan):
- Describe the scope and suggest which ROK systems are affected

**Research Further** (difficulty 4-5 or low confidence):
- Pose specific research questions to answer first

**Memory Candidates** (insights worth persisting):
- Provide ready-to-use `/memory-write` commands

### Step 6: Cross-Reference ROK Memory

If the Supabase memory system is accessible:
1. For each recommendation, query related existing memories:
   - `/memory-query category:"decision"` for relevant keywords
   - `/memory-query category:"pattern"` for relevant keywords
   - `/memory-query category:"gotcha"` for relevant keywords
2. Flag any conflicts with existing ROK decisions
3. Note any reinforcement of existing patterns
4. Identify resolutions for known gotchas

If memory system is unavailable, note: "Memory cross-reference: skipped (Supabase unavailable)"

### Step 7: Save to Knowledge Library

Read `~/.claude/youtube-intelligence/library.json`. If it doesn't exist, create it with `{"videos": []}`.

Append a new entry:
```json
{
  "video_id": "[ID from URL or generated slug]",
  "title": "[title]",
  "channel": "[channel]",
  "url": "[URL if available]",
  "analyzed": "[ISO date]",
  "type": "[classification from Step 3]",
  "topics": ["[topics from Step 3]"],
  "trust_weight": "[trust tier]",
  "key_points_count": "[count]",
  "claims_count": "[count]",
  "recommendations_count": "[count]",
  "analysis_path": "[path if saved to file]",
  "brief_generated": false
}
```

Also update the creator's `videos_analyzed` count in `creators.json` if the channel was in the registry.

### Step 8: Present Results

Display the full analysis report:

```markdown
═══════════════════════════════════════════════════════
YOUTUBE INTELLIGENCE ANALYSIS
═══════════════════════════════════════════════════════

## Video Analysis: [Title]

**Channel:** [name] [TRUSTED CREATOR badge if applicable]
**Published:** [date] | **Duration:** [length] | **Type:** [classification]
**Transcript Quality:** [HIGH/MEDIUM/LOW]
**Trust Weight:** [tier] - [reason]
**Analysis Depth:** [quick/standard/deep]

---

### Key Points
1. **[Statement]** (confidence: [level], actionability: [level])
   - Evidence: "[quote or paraphrase]"

2. **[Statement]** ...

[up to 10 key points]

---

### Technical Details
| Tool/Library | Version | Context | Docs |
|-------------|---------|---------|------|
[if applicable]

### Code Patterns & Commands
[if applicable - extracted snippets, CLI commands, configurations]

---

### Validated Claims
| Claim | Status | Score | Source |
|-------|--------|-------|--------|
[if standard/deep depth]

---

### ROK Integration Recommendations

**Overall Confidence:** [HIGH/MEDIUM/LOW]

#### Immediate Actions (can do now)
- [Action]: [specific instruction, where in ROK]

#### Requires Planning (/2_plan)
- [Action]: [scope, complexity, affected systems]

#### Research Further
- [Topic]: [why, what questions to answer]

#### Memory Candidates
```
/memory-write category:"pattern" key:"[key]" value:"[insight] (source: [channel] [date])"
```

---

### Additional Resources
[From validation research - official docs, repos, related articles]

═══════════════════════════════════════════════════════

## Next Steps
- Export to HTML/PDF/MD: `/yt-export`
- Generate implementation brief: `/yt-brief`
- Save insights to memory: use the /memory-write commands above
- Analyze related videos: `/yt-batch topic:"[detected topic]"`
- Start full planning session: `/yt-brief format:research-input` then `/2_plan`
```

## Important Rules

- NEVER fabricate transcript content or quotes
- NEVER assume what a video says without having the transcript
- If transcript quality is poor, clearly caveat the analysis
- Always attribute insights to their source (video + approximate position)
- For `quick` depth, skip validation research entirely
- For `standard` depth, validate claims + verify tools
- For `deep` depth, do everything including related content discovery
- If the video is not relevant to ROK at all (e.g., pure entertainment), still summarize but note "No ROK recommendations identified"
