# Plugin Idea Shortlist

Recall and filter the most recently generated plugin idea shortlist.

## Usage

```
/plugin-idea-generator:idea-shortlist                      # Show full list
/plugin-idea-generator:idea-shortlist --tier=BUILD_NOW     # Filter by tier
/plugin-idea-generator:idea-shortlist --pathway=saas_app   # Filter by product pathway
/plugin-idea-generator:idea-shortlist --top=5              # Show only top N
```

## Arguments

- **--tier** (optional): Filter by tier: `BUILD_NOW`, `STRONG`, `BACKLOG`, `PASS`
- **--pathway** (optional): Filter by product pathway: `saas_app`, `chrome_extension`, `api_service`, `marketplace_plugin`, `mobile_app`, `hybrid`
- **--top** (optional): Show only top N results

Initial request: $ARGUMENTS

## Workflow

1. **Read shortlist**: Load `/tmp/plugin_ideas_shortlist.json`
   - If file doesn't exist, inform user: "No shortlist found. Run `/plugin-idea-generator:generate-ideas` first."

2. **Parse filters**: Extract `--tier`, `--pathway`, `--top` from $ARGUMENTS.

3. **Apply filters**: Filter the shortlist array by matching criteria.

4. **Display**: Present filtered results using the same table format as generate-ideas:

```
## Plugin Idea Shortlist [Filter Applied]

**Generated**: [date] | **Depth**: [depth] | **Topic**: [topic]
**Showing**: [N of M total ideas] [filter description]

| # | Plugin Idea | Tier | Score | Utility | Market | Novelty | Pathway | Extends |
|---|-------------|------|-------|---------|--------|---------|---------|---------|
| ... |

### Detail (filtered ideas)

**#N: [Display Name]** (TIER - Score)
> [One-liner]
- **Build it**: `/plugin-dev:create-plugin [slug-name]`
```

5. **If no results match filter**: "No ideas match the filter `--tier=BUILD_NOW`. Available tiers in this shortlist: STRONG (5), BACKLOG (4), PASS (2)."

## Rules
- Read-only. Never modify the shortlist file.
- If the shortlist file is missing, direct user to generate-ideas.
- Always include the `create_prompt` field so users can immediately act on an idea.
