---
name: case-ingest
description: |
  Scan a folder for PDF files and ingest into the Legal Case Builder database.
  Extracts text, detects document types, parses email metadata, generates
  AI summaries, and auto-categorizes with topic tags.
triggers:
  - "case ingest"
  - "ingest documents"
  - "import pdfs"
  - "add documents"
  - "document intake"
version: 1.2
author: ROK Agency
---

# Case Ingest

Scan a folder for PDF files and ingest into the Legal Case Builder database.

## Usage

```
/legal-case-builder:case-ingest                     # Default case folder
/legal-case-builder:case-ingest folder:/path/to/pdfs force:true
```

## When to Use

- When you need to invoke /legal-case-builder:case-ingest
- When the user's request matches the trigger keywords above
