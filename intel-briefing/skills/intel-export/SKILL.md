---
name: intel-export
description: |
  Export intelligence reports to HTML, PDF, and Markdown formats. Supports
  exporting master briefings, prediction tracking reports, and accuracy
  analyses. Files saved to Desktop output folder.
triggers:
  - "intel export"
  - "export briefing"
  - "export report"
  - "export predictions"
  - "export accuracy"
  - "intelligence export"
version: 1.2
author: ROK Agency
---

# Intel Export

Export intelligence briefings and reports to multiple formats.

## Usage

```
/intel-briefing:intel-export briefing              # Export master briefing (all formats)
/intel-briefing:intel-export predictions            # Export prediction tracking report
/intel-briefing:intel-export accuracy               # Export accuracy analysis report
/intel-briefing:intel-export briefing format:html   # Specific format only
/intel-briefing:intel-export briefing format:pdf
/intel-briefing:intel-export briefing format:md
```

## When to Use

- Generating shareable reports from the intelligence system
- Creating PDF briefings for offline review
- Exporting accuracy data for external analysis
