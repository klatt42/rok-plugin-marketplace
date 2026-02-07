# /yt-library - Knowledge Library Browser

Browse, search, and recall previously analyzed YouTube videos. Enables re-accessing insights without re-analyzing and provides statistics on your learning patterns.

## Usage

```
/yt-library                                  # Show recent analyses
/yt-library search:"MCP server"              # Search by title, channel, or topic
/yt-library topic:"ai-agents"                # Filter by topic tag
/yt-library channel:"Cole Medin"             # Filter by channel
/yt-library since:2026-01-01                 # Filter by analysis date
/yt-library stats                            # Show library statistics
```

### Parameters
- **(no args)** - Display recent analyses (last 20)
- **search** - Full-text search across title, channel, and topics
- **topic** - Filter by specific topic tag
- **channel** - Filter by channel name (case-insensitive)
- **since** - Show only analyses after this date (YYYY-MM-DD)
- **stats** - Show aggregated statistics instead of video list

## Execution Steps

### Step 1: Load Library

Read `~/.claude/youtube-intelligence/library.json`.

If the file does not exist or is empty:
```
YouTube Intelligence Library is empty.

Get started by analyzing a video:
  /yt-analyze url:https://youtube.com/watch?v=...

Or paste a transcript directly:
  /yt-analyze
  [paste transcript]
```

### Step 2: Apply Filters

**No args:** Sort by `analyzed` date descending, limit to 20 most recent.

**search:** Case-insensitive search across `title`, `channel`, and `topics` array. Return all matches.

**topic:** Exact match (case-insensitive) against entries in the `topics` array.

**channel:** Case-insensitive match against `channel` field.

**since:** Filter entries where `analyzed` >= provided date.

Multiple filters can be combined: `/yt-library channel:"Cole Medin" since:2026-01-01`

### Step 3: Display Results

#### Standard View (video list)

```markdown
## YouTube Intelligence Library

**Total videos analyzed:** [count]
**Topics covered:** [unique topic count]
**Trusted creator videos:** [count where trust_weight != "STANDARD"]

### Analyses [filter description if filtered]

| # | Title | Channel | Date | Type | Topics | Trust | Brief? |
|---|-------|---------|------|------|--------|-------|--------|
| 1 | [title] | [channel] | [date] | tutorial | ai, mcp | HIGH | Yes |
| 2 | [title] | [channel] | [date] | news | agents | STD | No |
| ... |

### Quick Actions
- Re-read an analysis: `Read [analysis_path]`
- Generate a brief from any analysis: `/yt-brief source:[analysis_path]`
- Find related videos: `/yt-batch topic:"[topic]"`
- Check what's new from a creator: `/yt-batch channel:"[name]"`
- View statistics: `/yt-library stats`
```

If the list is longer than 20 entries, show:
```
Showing 20 of [total]. Use filters to narrow: /yt-library topic:"[topic]" or /yt-library since:[date]
```

#### Stats View

When `stats` parameter is provided:

```markdown
## YouTube Intelligence Statistics

**Library Created:** [date of first entry]
**Total Videos Analyzed:** [count]
**Total Briefs Generated:** [count where brief_generated == true]

### By Topic
| Topic | Count | Last Analyzed |
|-------|-------|---------------|
| ai-agents | 12 | 2026-02-05 |
| claude-code | 8 | 2026-02-06 |
| mcp | 5 | 2026-02-01 |
| ... |

### By Channel
| Channel | Count | Trust | Last Analyzed |
|---------|-------|-------|---------------|
| Cole Medin | 6 | HIGH | 2026-02-06 |
| IndyDevDan | 4 | HIGH | 2026-02-03 |
| [other] | 3 | STD | 2026-02-01 |

### By Content Type
| Type | Count | Percentage |
|------|-------|------------|
| tutorial | 8 | 40% |
| thought-leadership | 5 | 25% |
| news | 4 | 20% |
| demo-walkthrough | 3 | 15% |

### By Month
| Month | Videos | Briefs Generated |
|-------|--------|-----------------|
| 2026-02 | 5 | 2 |
| 2026-01 | 12 | 4 |

### Insights
- **Most analyzed topic:** [topic] ([count] videos)
- **Most watched creator:** [channel] ([count] videos)
- **Brief conversion rate:** [briefs/total]% of analyses led to implementation briefs
- **Average recommendations per video:** [avg]
```

## Important Rules

- The library is read-only through this command - it's populated by `/yt-analyze` and updated by `/yt-brief`
- If a referenced analysis_path no longer exists (file was moved/deleted), note it but still show the library entry
- Keep the display scannable - use tables, not paragraphs
- Stats should reveal learning patterns (what topics the user gravitates toward, which creators they follow most)
- Never modify library.json through this command
