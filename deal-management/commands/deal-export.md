# Deal Export

You are exporting pipeline deals to professional Excel and PDF reports.

## Input

The user may provide:
- **Pipeline name** (default: general_sales)
- **Status filter** (active, won, lost, all — default: active)

## Process

### Step 1: Get Pipeline Data

Call `get_pipeline` to retrieve all deals:

```
get_pipeline(pipeline="general_sales", status_filter="active")
```

### Step 2: Prepare Export Data

Construct a JSON payload for the export script:

```json
{
  "type": "pipeline",
  "pipeline_name": "[pipeline]",
  "carrier": "[Pipeline Name]",
  "region": "Pipeline Report",
  "date": "[YYYY-MM-DD]",
  "report_type": "Pipeline",
  "search_summary": "Pipeline export: [pipeline] — [count] active deals, $[value] total value",
  "stages": [
    {
      "name": "[stage]",
      "deal_count": [n],
      "total_value": [value],
      "deals": [
        {
          "id": [id],
          "title": "[title]",
          "company": "[company]",
          "contact": "[contact]",
          "value": [value],
          "probability": [prob],
          "status": "[status]",
          "expected_close": "[date]"
        }
      ]
    }
  ],
  "records": [flat array of all deals for table export],
  "analysis": "[Summary of pipeline health]",
  "next_steps": ["[action 1]", "[action 2]"]
}
```

### Step 3: Run Export

Write the JSON to a temp file and run the export:

```bash
cat > /tmp/pipeline_export.json << 'EXPORT_EOF'
{ ... the JSON payload ... }
EXPORT_EOF

~/.claude/scripts/.venv/bin/python3 ~/.claude/scripts/prospecting_export.py \
  --input /tmp/pipeline_export.json

rm /tmp/pipeline_export.json
```

### Step 4: Report Output

```
## Export Complete

- **Excel**: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/[Pipeline]/[filename].xlsx
- **PDF**: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/[Pipeline]/[filename].pdf
- **Deals Exported**: [count]
- **Total Value**: $[value]
```

## Rules

- Default to active deals only
- Include all stages in the export, even empty ones
- Sort deals by stage position, then by value descending
- Use the pipeline name as the folder grouping
- Date format: YYYY-MM-DD for filenames
