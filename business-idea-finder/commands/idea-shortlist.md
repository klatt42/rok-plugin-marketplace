# Idea Shortlist — View and Filter Last Results

Recall, filter, and re-rank the most recent idea finder shortlist. Useful for reviewing results after a break or narrowing down ideas for analysis.

## Usage

```
/business-idea-finder:idea-shortlist                        # Show full last shortlist
/business-idea-finder:idea-shortlist --tier=HOT             # Filter to HOT tier only
/business-idea-finder:idea-shortlist --mode=arbitrage       # Show only arbitrage-sourced ideas
/business-idea-finder:idea-shortlist --type=extension       # Filter by opportunity type
```

## Arguments

- **--tier** (optional): Filter by tier — `HOT`, `WARM`, `WATCH`, `PASS`
- **--mode** (optional): Filter by discovery mode — `pain-points`, `gaps`, `arbitrage`, `cross-pollination`
- **--type** (optional): Filter by opportunity type — `SaaS`, `extension`, `API`, `automation`

Initial request: $ARGUMENTS

## Workflow

1. **Load shortlist**: Read `/tmp/idea_finder_shortlist.json`. If not found, inform the user: "No shortlist found. Run `/business-idea-finder:find-ideas` first."

2. **Apply filters**: If any filter flags are provided, filter the shortlist accordingly. Multiple filters are AND-combined.

3. **Display**:
   - Show the filtered shortlist table (same format as find-ideas output)
   - Show detail for top 3 in the filtered set
   - Include the `analyze_prompt` for each so the user can copy-paste into the analyzer

4. **Offer actions**:
```
Options:
a) Analyze an idea: /business-idea-analyzer:analyze-idea [paste from above]
b) Export this shortlist to MD/PDF/HTML
c) Re-run finder with different scope
d) Clear shortlist
```

## Rules

- This is a display/filter command only. No new research.
- If the shortlist JSON is missing or corrupt, suggest re-running the finder.
- Preserve the original scores — do not re-score on recall.
