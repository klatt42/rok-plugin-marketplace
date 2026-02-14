---
name: intel-ingest
description: |
  Ingest documents into the intelligence briefing system. Extracts claims,
  predictions, and key points from files or URLs. Validates against external
  sources, stores in Supabase, and optionally triggers master briefing update.
  Supports YouTube transcripts, articles, PDFs, and markdown files.
triggers:
  - "intel ingest"
  - "ingest document"
  - "process document"
  - "add intelligence"
  - "ingest transcript"
  - "ingest article"
version: 1.2
author: ROK Agency
---

# Intel Ingest

Ingest a document into the intelligence briefing system.

## Usage

```
/intel-briefing:intel-ingest <path-or-url>
/intel-briefing:intel-ingest                    # Process watch folder
/intel-briefing:intel-ingest --skip-validation   # Skip external validation
/intel-briefing:intel-ingest --skip-briefing     # Don't update master briefing
```

## When to Use

- Processing a new YouTube transcript, article, or PDF
- Batch processing files from the watch folder
- Adding new source material to the intelligence database
