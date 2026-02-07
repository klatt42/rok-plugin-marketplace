# /yt-batch - Batch Analyze Multiple YouTube Videos

Analyze multiple videos on a topic to build comprehensive understanding. Uses parallel subagent dispatch for efficiency and produces a synthesized cross-video report with consensus detection, conflict identification, and a suggested learning path.

## Usage

```
/yt-batch topic:"Claude Code MCP servers"
/yt-batch urls:https://youtube.com/watch?v=abc,https://youtube.com/watch?v=def
/yt-batch channel:"Cole Medin" limit:5
/yt-batch topic:"agentic workflows" depth:standard limit:3
```

### Parameters
- **topic** - Search YouTube for videos on this topic and analyze top results
- **urls** - Comma-separated list of specific YouTube URLs to analyze
- **channel** - Analyze recent videos from a specific channel
- **limit** - Maximum videos to analyze (default: 5, max: 10)
- **depth** - Per-video analysis depth: `quick` (default for batch) | `standard`

## Execution Steps

### Step 1: Collect Video URLs

Based on the input method:

**If `topic:` provided:**
1. Use WebSearch for `"YouTube [topic]"` to find relevant videos
2. Also try `"site:youtube.com [topic]"` for direct YouTube results
3. Collect unique video URLs up to the limit
4. For each URL, use WebFetch to get the title and channel name

**If `urls:` provided:**
1. Parse the comma-separated URL list
2. Validate each is a YouTube URL
3. Use WebFetch on each to get title and channel name

**If `channel:` provided:**
1. Use WebSearch for `"site:youtube.com [channel name]"` to find recent uploads
2. Collect unique video URLs up to the limit
3. Use WebFetch on each to get title and publish date

### Step 2: Approval Gate

ALWAYS present the batch plan before proceeding:

```markdown
═══════════════════════════════════════════════════════
BATCH ANALYSIS PLAN
═══════════════════════════════════════════════════════

Videos to analyze: [count]
Depth per video: [quick/standard]
Topic focus: [topic or "varied"]

| # | Title | Channel | URL |
|---|-------|---------|-----|
| 1 | [title] | [channel] | [url] |
| 2 | [title] | [channel] | [url] |
| ... |

Proceed with batch analysis? (This will use parallel subagents)
═══════════════════════════════════════════════════════
```

**Wait for user approval before proceeding.** If the user wants to modify the list, adjust and re-present.

### Step 3: Dispatch Parallel Analysis

For each approved video, attempt to get transcripts. Then for each video that has usable content, spawn a **transcript-analyst** subagent using the Task tool with `run_in_background: true`:

```
For each video:
  Task tool:
    subagent_type: general-purpose
    prompt: [Include transcript-analyst agent instructions + video transcript + metadata]
    run_in_background: true
```

This runs all analyses in parallel for efficiency.

### Step 4: Collect Results

Use TaskOutput to gather results from all background subagents. Track which completed successfully and which failed.

If any videos failed to analyze (no transcript, subagent error), note them:
```
Analyzed: [X] of [Y] videos
Failed: [list of failed videos with reasons]
```

### Step 5: Cross-Video Synthesis

Using the insight-synthesis skill methodology, produce a unified report:

**5a. Consensus Detection:**
- Identify insights mentioned by 2+ videos
- These get the highest confidence boost
- Note which specific videos agree

**5b. Unique Insights:**
- Insights from only one video
- Still valuable but need the validation context from that single source

**5c. Conflict Detection:**
- Where videos disagree on an approach or claim
- Present both sides without picking a winner
- Note creator trust levels for context

**5d. Trending Themes:**
- Topics that appear across multiple videos, even if discussed differently
- Group by theme, note frequency

**5e. Tools & Technologies Roll-up:**
- Aggregate all tools mentioned across videos
- Note how many videos mention each tool
- Highlight tools mentioned by trusted creators

**5f. Combined Recommendations:**
- Merge and deduplicate recommendations from all videos
- Priority order by: consensus count, creator trust, validation score
- Remove duplicates (same recommendation from different videos)

**5g. Learning Path:**
- Order videos from foundational to advanced
- Identify prerequisite concepts
- Suggest watch order for progressive understanding
- Insert non-video resources (docs, repos) where helpful

### Step 6: Save Results

Save the batch synthesis report to:
`thoughts/shared/research/yt-batch-[topic-slug]-[date].md`

Update the knowledge library (`~/.claude/youtube-intelligence/library.json`) with entries for each analyzed video.

### Step 7: Present Report

```markdown
═══════════════════════════════════════════════════════
BATCH ANALYSIS: [Topic]
═══════════════════════════════════════════════════════

**Videos analyzed:** [count] | **Date:** [date]
**Videos by trusted creators:** [count]

---

### Consensus Points (mentioned by 2+ videos)
- **[Point]** - mentioned in: [Video A], [Video C] | confidence: HIGH
- **[Point]** - mentioned in: [Video B], [Video D] | confidence: HIGH

### Unique Insights (single source)
- **[Insight]** (from [Video B] by [Channel]) | confidence: [based on trust + validation]

### Conflicting Views
- **[Topic]:** [Video A] recommends X, while [Video D] recommends Y
  - Context: [why they disagree]

### Trending Themes
| Theme | Videos | Frequency |
|-------|--------|-----------|
| [Theme 1] | A, B, C | 3/[total] |

### Tools & Technologies Mentioned
| Tool | Videos Mentioning | Context |
|------|-------------------|---------|
| [Tool] | [count] | [primary use case] |

---

### Combined ROK Recommendations (priority order)

#### High Priority (consensus + trusted + validated)
1. [Recommendation] - Sources: [videos] - Confidence: HIGH

#### Medium Priority
2. [Recommendation] - Source: [video] - Confidence: MEDIUM

#### Explore Further
3. [Topic] - mentioned by [video], needs more research

---

### Suggested Learning Path
Watch in this order for progressive understanding:

1. **[Video Title]** by [Channel] - Foundational concepts
   - Key takeaway: [one sentence]

2. **[Official Docs URL]** - Reference reading before next video

3. **[Video Title]** by [Channel] - Builds on #1
   - Key takeaway: [one sentence]
   - Prerequisites: Concepts from #1

---

## Next Steps
- Export to HTML/PDF/MD: `/yt-export`
- Generate implementation brief from top recommendations: `/yt-brief`
- Deep-dive a specific video: `/yt-analyze url:[url] depth:deep`
- Browse all analyzed videos: `/yt-library`
- Save batch insights to memory: [suggested /memory-write commands]

═══════════════════════════════════════════════════════
```

## Important Rules

- ALWAYS show the approval gate before starting batch analysis
- Use `quick` depth by default for batch to manage token usage
- Maximum 10 videos per batch - suggest splitting larger requests
- If a video's transcript can't be obtained, skip it and note the skip
- Deduplication is critical - same insight from 3 videos should appear once with all 3 cited
- Learning path should be practical, not just chronological
- Credit all creators for their contributions to the synthesis
