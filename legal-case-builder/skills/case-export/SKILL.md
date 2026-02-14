---
name: case-export
description: |
  Export case data as formatted HTML, PDF, and Markdown reports suitable
  for attorney review, case filing, or archival. Supports timeline,
  claims, brief, and full export types.
triggers:
  - "case export"
  - "export case"
  - "legal report"
  - "case report"
  - "attorney report"
version: 1.2
author: ROK Agency
---

# Case Export

Export case data as formatted HTML, PDF, and Markdown reports suitable

## Usage

```
/legal-case-builder:case-export type:full           # Export everything
/legal-case-builder:case-export type:timeline format:pdf
```

## When to Use

- When you need to invoke /legal-case-builder:case-export
- When the user's request matches the trigger keywords above
