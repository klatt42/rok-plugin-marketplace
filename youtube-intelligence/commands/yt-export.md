# /yt-export - Export Analysis to HTML, PDF, and Markdown

Exports a YouTube Intelligence analysis to formatted HTML (viewable in Chrome), PDF, and Markdown files. Files are saved to the Desktop output folder with unique names.

## Usage

```
/yt-export                                    # Export most recent analysis (all formats)
/yt-export source:thoughts/shared/research/yt-cole-medin-analysis.md
/yt-export format:html                        # Only HTML
/yt-export format:pdf                         # Only PDF
/yt-export format:md                          # Only Markdown
/yt-export format:all                         # All 3 (default)
```

### Parameters
- **source** - Path to a specific analysis file (default: most recent from session)
- **format** - `all` (default) | `html` | `pdf` | `md` | comma-separated like `html,pdf`

## Output Location

All files are saved to:
```
C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\YouTube-Intelligence\
```
(WSL path: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/YouTube-Intelligence/`)

### File Naming
Files use the pattern: `{YYYY-MM-DD}_{slugified-title}_{type}.{ext}`

Example:
```
2026-02-07_cole-medin-mcp-servers_analysis.html
2026-02-07_cole-medin-mcp-servers_analysis.pdf
2026-02-07_cole-medin-mcp-servers_analysis.md
```

## Execution Steps

### Step 1: Determine Source Content

1. If `source:` parameter provided, read the specified file
2. If no source, use the most recent `/yt-analyze`, `/yt-brief`, or `/yt-batch` output from the current session
3. If no analysis is available:
   ```
   No analysis found to export. Run one of these first:
   - /yt-analyze url:<YouTube URL>
   - /yt-brief
   - /yt-batch topic:"<topic>"
   ```

### Step 2: Build Export JSON

Transform the analysis content into the structured JSON format expected by the export script. Parse the analysis output and build sections:

```json
{
  "type": "analysis|brief|batch",
  "title": "[Video title or topic]",
  "channel": "[Creator name]",
  "date": "[Today's date: YYYY-MM-DD]",
  "url": "[YouTube URL if available]",
  "trust_weight": "HIGH|MEDIUM|STANDARD",
  "classification": "[Content type classification]",
  "sections": []
}
```

**Section mapping from analysis output:**

For `/yt-analyze` output, create sections:
- **Key Points** (type: bullets) - from the Key Points section
- **Technical Details** (type: table, headers: ["Tool", "Version", "Context"]) - if present
- **Code Patterns & Commands** (type: text) - if present
- **Validated Claims** (type: table, headers: ["Claim", "Status", "Score"]) - if validation was run
- **Immediate Actions** (type: bullets) - from ROK recommendations
- **Requires Planning** (type: bullets) - from ROK recommendations
- **Research Further** (type: bullets) - from ROK recommendations
- **Memory Candidates** (type: bullets) - from ROK recommendations
- **Additional Resources** (type: bullets) - from validation research

For `/yt-brief` output, create sections:
- **Problem/Opportunity** (type: text)
- **Proposed Changes** (type: bullets)
- **Supporting Research** (type: bullets)
- **Risks** (type: table, headers: ["Risk", "Impact", "Mitigation"])
- **Suggested Next Step** (type: text)

For `/yt-batch` output, create sections:
- **Consensus Points** (type: bullets)
- **Unique Insights** (type: bullets)
- **Conflicting Views** (type: bullets)
- **Trending Themes** (type: table, headers: ["Theme", "Videos", "Frequency"])
- **Tools & Technologies** (type: table, headers: ["Tool", "Videos Mentioning", "Context"])
- **Combined Recommendations** (type: bullets)
- **Learning Path** (type: bullets)

### Step 3: Determine Formats

Parse the `format:` parameter:
- `all` or not specified: `["html", "pdf", "md"]`
- Single format: `["html"]`, `["pdf"]`, or `["md"]`
- Comma-separated: split and validate each

### Step 4: Write JSON and Run Export Script

1. Write the JSON payload to a temp file:
   ```python
   # Use the scratchpad directory for temp files
   temp_path = "/tmp/claude-1000/.../scratchpad/yt_export_data.json"
   ```

2. Run the export script:
   ```bash
   python3 ~/.claude/scripts/youtube_export.py --input <temp_path> --formats <format_list>
   ```

3. Parse the script's JSON output for file paths.

### Step 5: Report Results

Display the generated file paths to the user:

```markdown
═══════════════════════════════════════════════════════
EXPORT COMPLETE
═══════════════════════════════════════════════════════

**Title:** [title]
**Type:** [analysis/brief/batch]
**Output folder:** C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\YouTube-Intelligence\

Generated files:
- HTML: [filename].html  (open in Chrome to view)
- PDF:  [filename].pdf
- MD:   [filename].md

Windows path: C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\YouTube-Intelligence\
═══════════════════════════════════════════════════════
```

### Step 6: Offer to Open HTML

After export, suggest:
```
To open the HTML report in Chrome, you can:
- Navigate to the Desktop folder: Claude Code Plugin Output > YouTube-Intelligence
- Double-click the .html file
```

## Important Rules

- Always use the scratchpad directory for temp JSON files, never the project directory
- The export script handles file naming and folder creation - do not create folders manually
- If the export script fails, display the error and suggest checking that the venv is set up
- Each export generates unique filenames based on date + title + type, so no overwrites
- The HTML file is self-contained with embedded CSS - no external dependencies
- PDF uses Helvetica (built into fpdf2) - no font installation needed
- Markdown includes YAML frontmatter for metadata
