# SEO Report

You are generating an export report from SEO audit data collected in the current session. Your goal is to format the data and produce professional Excel and/or PDF files.

## Input

The user will provide:
- **Format** (optional) — `pdf`, `excel`, or `all` (default: `all`)
- **Data source** — from current session audit data (optimize-page or batch-audit results)

If no audit data exists in the current session, inform the user:
"No SEO audit data found in this session. Run `/optimize-page [url]` or `/batch-audit [source]` first, then use `/seo-report` to export."

## Process

### Step 1: Gather Session Data

Collect all audit data from the current session:
- Page scores and elements from optimize-page runs
- Batch audit results if batch-audit was run
- Issues and recommendations
- Score summaries

### Step 2: Construct Export Payload

Build the `type: "seo_audit"` JSON payload:

```json
{
  "type": "seo_audit",
  "carrier": "[site domain]",
  "region": "[target area or 'All']",
  "date": "YYYY-MM-DD",
  "report_type": "SEO_Audit",
  "search_summary": "SEO audit of [X] pages on [domain]",
  "records": [
    {
      "url": "https://...",
      "score": 72,
      "title": "Current Title",
      "title_length": 55,
      "meta_description": "Current meta...",
      "meta_length": 148,
      "h1": "Page Heading",
      "word_count": 720,
      "issues_count": 5,
      "priority": "high"
    }
  ],
  "issues": [
    {
      "url": "https://...",
      "issue": "Missing canonical tag",
      "severity": "critical",
      "current": "No canonical found",
      "recommended": "Add self-referencing canonical"
    }
  ],
  "analysis": "Key findings summary",
  "next_steps": ["Fix critical issues", "Optimize content", "Add schema"],
  "score_summary": {
    "total_pages": 25,
    "avg_score": 74,
    "excellent": 3,
    "good": 8,
    "needs_work": 7,
    "poor": 4,
    "critical": 3
  }
}
```

### Step 3: Write and Execute

```bash
# Write payload to temp file
cat > /tmp/seo_audit_export.json << 'EXPORT_EOF'
{ ... payload ... }
EXPORT_EOF

# Run export script
~/.claude/scripts/.venv/bin/python3 ~/.claude/scripts/prospecting_export.py \
  --input /tmp/seo_audit_export.json

# Clean up
rm /tmp/seo_audit_export.json
```

### Step 4: Report Results

Display the output paths:

```
## Export Complete

- Excel: [path to .xlsx]
- PDF: [path to .pdf]
- Records exported: XX pages
- Output folder: Desktop/Claude Code Plugin Output/SEO_Reports/
```

The Excel file contains 4 sheets:
1. **Page Scores** — all pages with scores and key metrics
2. **Issues** — all issues sorted by severity
3. **Recommendations** — prioritized action items
4. **Analysis** — summary, methodology, next steps

The PDF contains:
- Executive summary with score distribution
- Top issues table
- Priority pages requiring attention
- Next steps

## Rules

- Only export data that was collected in the current session
- If no data exists, tell the user to run an audit first
- Use today's date for the report date
- Sort records by score ascending (worst first)
- Sort issues by severity (critical > high > medium > low)
- Clean up temp files after export
- Report exact output file paths to the user
