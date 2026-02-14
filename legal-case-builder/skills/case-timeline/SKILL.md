---
name: case-timeline
description: |
  Generate a chronological timeline of events from the case database.
  Events are extracted from documents and linked to source materials.
  Supports date ranges, tag filtering, and multiple output formats.
triggers:
  - "case timeline"
  - "legal timeline"
  - "event timeline"
  - "chronology"
  - "case history"
version: 1.2
author: ROK Agency
---

# Case Timeline

Generate a chronological timeline of events from the case database.

## Usage

```
/legal-case-builder:case-timeline                   # Full timeline
/legal-case-builder:case-timeline from:2024-01-01 focus:hvac_defect
```

## When to Use

- When you need to invoke /legal-case-builder:case-timeline
- When the user's request matches the trigger keywords above
