# /intel-export - Export Intelligence Reports

Export intelligence briefings, prediction tracking reports, and accuracy analyses to HTML, PDF, and Markdown formats. Files are saved to the Desktop output folder.

## Usage

```
/intel-briefing:intel-export briefing              # Export current master briefing (all formats)
/intel-briefing:intel-export predictions            # Export prediction tracking report
/intel-briefing:intel-export accuracy               # Export accuracy analysis report
/intel-briefing:intel-export briefing format:html   # Specific format only
/intel-briefing:intel-export briefing format:pdf    # PDF only
/intel-briefing:intel-export briefing format:md     # Markdown only
/intel-briefing:intel-export briefing format:html,pdf  # Multiple specific formats
```

### Parameters
- **Report type** (first argument) - `briefing` (default), `predictions`, `accuracy`
- **format** - `all` (default), `html`, `pdf`, `md`, or comma-separated list

Initial request: $ARGUMENTS

## Output Location

All files are saved to:
```
C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\Intel-Briefings\
```
(WSL path: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Intel-Briefings/`)

### File Naming
Files use the pattern: `{YYYY-MM-DD}_{report-type}_v{version}.{ext}`

Examples:
```
2026-02-11_intel-briefing_v5.html
2026-02-11_intel-briefing_v5.pdf
2026-02-11_intel-briefing_v5.md
2026-02-11_prediction-report.html
2026-02-11_accuracy-report.html
```

## Execution Steps

### Phase 1: Determine Report Type

Parse $ARGUMENTS for the report type:
- If first word is `briefing` or no type specified: report_type = `briefing`
- If first word is `predictions`: report_type = `predictions`
- If first word is `accuracy`: report_type = `accuracy`

Parse `format:` parameter:
- If not specified or `all`: formats = `["html", "pdf", "md"]`
- If single format: formats = `["html"]`, `["pdf"]`, or `["md"]`
- If comma-separated: split and validate each (e.g., `html,pdf` -> `["html", "pdf"]`)

### Phase 2: Gather Data from Supabase

#### For "briefing" report:

1. Query the latest briefing:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_briefings?order=version.desc&limit=1&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. If no briefing exists:
   ```
   No briefing found. Generate one first:
     /intel-briefing:intel-briefing refresh
   ```
   Stop here.

3. Build export payload matching the export script's expected format:
   ```json
   {
     "type": "briefing",
     "version": [version number],
     "date": "[today YYYY-MM-DD]",
     "document_count": [count],
     "new_since_last": [count],
     "prediction_count": [count],
     "executive_summary": "[text]",
     "key_developments": [array of development objects],
     "financial_section": {
       "market_outlook": {"short_term": "...", "medium_term": "..."},
       "sector_views": [array],
       "predictions": [array]
     },
     "geopolitical_section": {
       "section_summary": "...",
       "risk_matrix": [array],
       "predictions": [array]
     },
     "labor_section": {
       "section_summary": "...",
       "workforce_trends": [array],
       "predictions": [array]
     },
     "cross_domain_themes": [array],
     "consensus_themes": {object},
     "contested_topics": {object},
     "high_confidence_predictions": [array],
     "prediction_tracking": {
       "due_for_evaluation": [array],
       "recent_outcomes": [array],
       "accuracy_summary": {object}
     },
     "alert_matches": [array],
     "watch_items": [array],
     "full_briefing_md": "[complete markdown]"
   }
   ```

   Note: Parse the briefing record's JSON fields (consensus_themes, contested_topics, confidence_summary) and the text fields (executive_summary, financial_section, geopolitical_section, full_briefing_md) to construct this payload.

#### For "predictions" report:

1. Query all predictions:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?order=created_at.desc&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Build export payload:
   ```json
   {
     "type": "predictions",
     "date": "[today YYYY-MM-DD]",
     "predictions": [
       {
         "prediction_text": "...",
         "category": "...",
         "initial_confidence": 0.7,
         "timeframe": "6mo",
         "target_date": "2026-08-11",
         "outcome": "pending",
         "source_author": "..."
       }
     ]
   }
   ```

#### For "accuracy" report:

1. Query evaluated predictions:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?outcome=neq.pending&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Query sources for author accuracy:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_sources?select=source_name,trust_tier,prediction_accuracy,documents_analyzed" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

3. Calculate accuracy metrics and build payload:
   ```json
   {
     "type": "accuracy",
     "date": "[today YYYY-MM-DD]",
     "overall": {
       "total": [N],
       "evaluated": [N],
       "correct": [N],
       "accuracy": "[X]%",
       "brier": "[X.XXXX]"
     },
     "by_category": [
       {
         "category": "financial",
         "evaluated": [N],
         "correct": [N],
         "partial": [N],
         "incorrect": [N],
         "accuracy": "[X]%",
         "brier": "[X.XXXX]"
       }
     ],
     "by_source": [
       {
         "source": "[name]",
         "predictions": [N],
         "correct": [N],
         "accuracy": "[X]%",
         "trust_tier": "[tier]"
       }
     ]
   }
   ```

### Phase 3: Write Export JSON

Write the constructed payload to a temporary file:

```bash
# Write JSON payload to temp file
cat > /tmp/intel_briefing_export.json << 'EXPORT_EOF'
[JSON payload]
EXPORT_EOF
```

### Phase 4: Execute Export Script

Run the export script using the plugin's venv:

```bash
~/.claude/scripts/.venv/bin/python3 \
  ~/.claude/plugins/marketplaces/rok-plugin-marketplace/intel-briefing/scripts/intel_briefing_export.py \
  --input /tmp/intel_briefing_export.json \
  --type [briefing|predictions|accuracy] \
  --formats [all|html|pdf|md|html,pdf|etc]
```

Capture the script's JSON output which contains the generated file paths.

If the script fails:
```
Export script failed. Error: [error message]

Troubleshooting:
  1. Check venv exists: ls ~/.claude/scripts/.venv/bin/python3
  2. Check fpdf2 installed: ~/.claude/scripts/.venv/bin/python3 -c "from fpdf import FPDF; print('OK')"
  3. Check output directory is writable
```

### Phase 5: Clean Up and Report Results

1. Remove the temporary JSON file:
   ```bash
   rm -f /tmp/intel_briefing_export.json
   ```

2. Parse the script output for file paths and display results:
   ```
   =========================================
   EXPORT COMPLETE
   =========================================
   Report Type: [briefing/predictions/accuracy]
   Output Folder: C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\Intel-Briefings\

   Generated Files:
     HTML: [filename].html
     PDF:  [filename].pdf
     MD:   [filename].md

   Windows Path: C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\Intel-Briefings\
   =========================================

   To view:
     - Navigate to Desktop > Claude Code Plugin Output > Intel-Briefings
     - Double-click the .html file to open in Chrome
   ```

## Important Rules

- Always clean up `/tmp/intel_briefing_export.json` after export, even if the script fails
- Default to all formats (html, pdf, md) unless user specifies otherwise
- The export script handles file naming and folder creation -- do not create folders manually
- Each export generates unique filenames based on date + type + version, so no overwrites occur
- The HTML file is self-contained with embedded CSS -- no external dependencies needed
- PDF uses Helvetica (built into fpdf2) -- no font installation required
- If the briefing's full_briefing_md field is populated, the markdown export uses it directly
- For accuracy reports, only generate if there are evaluated predictions. If none exist, inform the user.
- The export script path is absolute: `~/.claude/plugins/marketplaces/rok-plugin-marketplace/intel-briefing/scripts/intel_briefing_export.py`
- The venv path is: `~/.claude/scripts/.venv/bin/python3`
