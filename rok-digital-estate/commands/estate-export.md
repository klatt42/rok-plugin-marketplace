# /estate-export - Re-Export Estate Snapshot

Re-export the most recent digital estate snapshot to HTML, PDF, and/or Markdown formats. Does not regenerate the snapshot -- just re-renders the existing one in the requested formats.

## Usage

```
/rok-digital-estate:estate-export                    # All formats (HTML, PDF, MD)
/rok-digital-estate:estate-export format:html        # HTML only
/rok-digital-estate:estate-export format:pdf         # PDF only
/rok-digital-estate:estate-export format:md          # Markdown only
/rok-digital-estate:estate-export format:html,pdf    # Multiple formats
/rok-digital-estate:estate-export gdrive             # Export + upload to Google Drive
```

### Parameters
- **format** - `all` (default), `html`, `pdf`, `md`, or comma-separated list
- **gdrive** - Upload to Google Drive after export (requires rclone)
- **gdrive-path** - Custom Google Drive path (default: `Digital-Estate/`)

Initial request: $ARGUMENTS

## Output Location

All files are saved to:
```
~/projects/rok-copilot/estate-snapshots/
```

### File Naming
Files use the pattern: `{YYYY-MM-DD}_estate-snapshot_v{version}.{ext}`

Examples:
```
2026-02-22_estate-snapshot_v3.html
2026-02-22_estate-snapshot_v3.pdf
2026-02-22_estate-snapshot_v3.md
```

## Execution Steps

### Phase 1: Find Latest Snapshot Data

1. Find the most recent snapshot markdown:
   ```bash
   LATEST=$(ls ~/projects/rok-copilot/estate-snapshots/*_estate-snapshot_v*.md 2>/dev/null | sort -V | tail -1)
   echo "FILE: $LATEST"
   ```

2. If no snapshot found:
   ```
   No estate snapshot found. Generate one first:
     /rok-digital-estate:generate-snapshot
   ```
   Stop here.

3. Read the snapshot file to get `full_estate_md` content.

4. Also check for the JSON data file (if export script saved one):
   ```bash
   JSON_FILE=$(echo "$LATEST" | sed 's/\.md$/.json/')
   test -f "$JSON_FILE" && echo "JSON_FOUND" || echo "JSON_MISSING"
   ```

### Phase 2: Parse Format Parameter

Parse $ARGUMENTS for format selection:
- If not specified or `all`: formats = `["html", "pdf", "md"]`
- If single format: formats = `["html"]`, `["pdf"]`, or `["md"]`
- If comma-separated: split and validate each

### Phase 3: Build Export Payload

Construct the JSON payload for the export script:

```json
{
  "type": "estate_snapshot",
  "version": [N],
  "date": "[YYYY-MM-DD]",
  "full_estate_md": "[complete markdown content]"
}
```

Write to temp file:
```bash
cat > /tmp/estate_snapshot_export.json << 'EXPORT_EOF'
[JSON payload]
EXPORT_EOF
```

### Phase 4: Execute Export Script

```bash
~/.claude/scripts/.venv/bin/python3 \
  ~/.claude/plugins/marketplaces/rok-plugin-marketplace/rok-digital-estate/scripts/estate_snapshot_export.py \
  --input /tmp/estate_snapshot_export.json \
  --output-dir ~/projects/rok-copilot/estate-snapshots/ \
  --formats [format list]
```

### Phase 5: Google Drive Upload (Optional)

If `gdrive` is in $ARGUMENTS:

1. Check rclone is available:
   ```bash
   which rclone && rclone listremotes 2>/dev/null | head -3
   ```

2. If available, upload:
   ```bash
   GDRIVE_PATH="${GDRIVE_PATH:-Digital-Estate}"
   rclone copy ~/projects/rok-copilot/estate-snapshots/*_estate-snapshot_v[N].* remote:"$GDRIVE_PATH/" --include "*.html" --include "*.pdf" --include "*.md"
   ```

3. If not available:
   ```
   Google Drive upload requires rclone. Setup:
     1. Install: sudo apt install rclone
     2. Configure: rclone config (choose Google Drive)
     3. Test: rclone ls remote:
   ```

### Phase 6: Clean Up and Report

1. Remove temp file:
   ```bash
   rm -f /tmp/estate_snapshot_export.json
   ```

2. Display results:
   ```
   =========================================
   EXPORT COMPLETE
   =========================================
   Snapshot Version: v[N]
   Output Folder: ~/projects/rok-copilot/estate-snapshots/

   Generated Files:
     HTML: [filename].html
     PDF:  [filename].pdf
     MD:   [filename].md

   Google Drive: [Uploaded to Digital-Estate/ / Skipped / rclone not configured]
   =========================================
   ```

## Important Rules

- Always clean up `/tmp/estate_snapshot_export.json` after export
- Default to all formats unless user specifies otherwise
- The export script handles file naming and folder creation
- Google Drive upload is optional and degrades gracefully
- NEVER include actual credentials in exported files
- If the export script fails, display troubleshooting steps
