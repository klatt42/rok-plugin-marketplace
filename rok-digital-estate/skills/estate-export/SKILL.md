---
name: estate-export
description: |
  Re-export an existing digital estate snapshot to HTML, PDF, and/or Markdown
  formats. Does not regenerate the snapshot, just re-renders the most recent
  one in the requested formats.
triggers:
  - "estate export"
  - "export snapshot"
  - "export estate"
  - "estate pdf"
  - "estate html"
version: 1.0
author: ROK Agency
---

# Estate Export

Re-export the latest estate snapshot to different formats.

## Usage

```
/rok-digital-estate:estate-export                    # All formats (HTML, PDF, MD)
/rok-digital-estate:estate-export format:html        # HTML only
/rok-digital-estate:estate-export format:pdf         # PDF only
/rok-digital-estate:estate-export format:md          # Markdown only
/rok-digital-estate:estate-export format:html,pdf    # Multiple formats
/rok-digital-estate:estate-export gdrive             # Export + upload to Google Drive
```

## When to Use

- Re-exporting a snapshot in a different format
- Sharing the estate document with family members
- Uploading to Google Drive for offsite backup
