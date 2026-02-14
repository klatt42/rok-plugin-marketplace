---
name: intel-library
description: |
  Browse and search the ingested document library. View all documents processed
  by the intelligence system with metadata, claim counts, trust assessments,
  and comprehensive statistics. Filter by source type, author, or date.
triggers:
  - "intel library"
  - "document library"
  - "browse documents"
  - "search documents"
  - "ingested documents"
  - "library stats"
version: 1.2
author: ROK Agency
---

# Intel Library

Browse, search, and get statistics on the ingested document library.

## Usage

```
/intel-briefing:intel-library                       # Show recent 20 documents
/intel-briefing:intel-library search:"gold"         # Full-text search
/intel-briefing:intel-library source_type:youtube    # Filter by type
/intel-briefing:intel-library author:"Peter Schiff"  # Filter by author
/intel-briefing:intel-library since:2026-01-01      # Filter by date
/intel-briefing:intel-library stats                 # Comprehensive statistics
/intel-briefing:intel-library document:[uuid]       # Full details for one doc
```

## When to Use

- Reviewing what documents have been processed
- Searching for specific topics across ingested content
- Checking ingestion statistics and source distribution
