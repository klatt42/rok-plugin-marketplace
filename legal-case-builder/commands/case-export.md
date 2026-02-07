# /case-export - Export Reports to HTML, PDF, and Markdown

Export case data as formatted reports to the Desktop output folder. Generates professional documents suitable for attorney review, case filing, or archival.

## Usage

```
/case-export type:timeline                       # Export timeline report
/case-export type:claims                         # Export claims with evidence
/case-export type:brief                          # Export legal brief
/case-export type:full                           # Export everything
/case-export type:timeline format:html           # Specific format only
/case-export type:timeline format:pdf
/case-export type:timeline format:md
/case-export type:timeline format:all            # All formats (default)
```

### Parameters
- **type** - `timeline` | `claims` | `brief` | `full`
- **format** - `all` (default) | `html` | `pdf` | `md`
- **from** - Start date filter for timeline exports
- **to** - End date filter for timeline exports
- **focus** - Tag topics to filter by

## Output Location

All files are saved to:
```
C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\Legal-Case-Builder\
```
(WSL path: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Legal-Case-Builder/`)

### File Naming
Files use the pattern: `{YYYY-MM-DD}_{report-type}_{case-name}.{ext}`

Example:
```
2026-02-07_timeline_rok-v-elion.html
2026-02-07_claims_rok-v-elion.pdf
2026-02-07_full-brief_rok-v-elion.md
```

## Execution Steps

### Step 1: Gather Data

Based on `type:` parameter, call the appropriate MCP tools:

**timeline:**
```
Tool: mcp__legal-case-builder__generate_timeline_report
Parameters: date_from, date_to, focus_topics, format: "legal_brief"
```

**claims:**
```
Tool: mcp__legal-case-builder__get_claims_summary
```

**brief:**
Call both `generate_timeline_report` (format: legal_brief) and `get_claims_summary`.

**full:**
Call `get_stats`, `generate_timeline_report`, and `get_claims_summary`.

### Step 2: Build Export Payload

Construct a JSON payload matching the export script format:
```json
{
  "type": "timeline|claims|brief|full",
  "title": "ROK Maryland LLC v. Elion Partners",
  "date": "2026-02-07",
  "sections": [
    {"heading": "...", "type": "bullets|table|text", ...}
  ],
  "formats": ["html", "pdf", "md"]
}
```

### Step 3: Generate Files

Write the JSON payload to a temp file in the scratchpad directory.

Call the export script:
```bash
python3 ~/.claude/scripts/youtube_export.py --input <temp.json>
```

Note: The youtube_export.py script handles all three format generation and file output.

Alternatively, generate Markdown directly and save to the output folder.

### Step 4: Report

```
═══════════════════════════════════════════════════════
EXPORT COMPLETE
═══════════════════════════════════════════════════════

Generated files:
  HTML: [filename.html]
  PDF:  [filename.pdf]
  MD:   [filename.md]

Location: C:\Users\...\Legal-Case-Builder\

Open in Chrome: [HTML path]
═══════════════════════════════════════════════════════
```

## Important Rules

- Ensure the output directory exists before writing files
- Use unique filenames with dates to prevent overwriting
- HTML should be self-contained with embedded CSS
- PDF should be professional quality for attorney use
- All exported documents should cite source document IDs
- For `full` type exports, include a table of contents
