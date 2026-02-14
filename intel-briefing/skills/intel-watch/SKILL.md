---
name: intel-watch
description: |
  Watch folder management for the intel-briefing system. Check and process files
  dropped into the designated watch folder for ingestion. Shows pending files,
  processed files, and can trigger batch ingestion of all pending documents.
triggers:
  - "intel watch"
  - "watch folder"
  - "pending files"
  - "process folder"
  - "batch ingest"
  - "watch status"
version: 1.2
author: ROK Agency
---

# Intel Watch

Manage the watch folder for document ingestion.

## Usage

```
/intel-briefing:intel-watch                        # Show pending files status
/intel-briefing:intel-watch status                 # Same as no args
/intel-briefing:intel-watch process                # Process all pending files
/intel-briefing:intel-watch process --skip-validation
/intel-briefing:intel-watch clean                  # Clean processed folder (>30 days)
```

## When to Use

- Checking if there are pending files to ingest
- Batch processing all files dropped into the watch folder
- Cleaning up old processed files
