---
name: case-search
description: |
  Search the Legal Case Builder database for documents matching a query.
  Supports full-text search, email topic filtering, date ranges, sender
  filtering, and thread reconstruction.
triggers:
  - "case search"
  - "search documents"
  - "find document"
  - "legal search"
  - "case documents"
version: 1.2
author: ROK Agency
---

# Case Search

Search the Legal Case Builder database for documents matching a query.

## Usage

```
/legal-case-builder:case-search query:"HVAC failure"
/legal-case-builder:case-search query:"rent credit" type:email sender:"Irina"
```

## When to Use

- When you need to invoke /legal-case-builder:case-search
- When the user's request matches the trigger keywords above
