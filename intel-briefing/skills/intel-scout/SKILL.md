---
name: intel-scout
description: |
  Automated daily intelligence content discovery. Searches for new content from
  watched creators, trending topics matching active briefing themes, and articles
  relevant to active predictions. Generates recommendation list for review and
  selective ingestion via /intel-ingest.
triggers:
  - "intel scout"
  - "content discovery"
  - "daily scan"
  - "find new content"
  - "scout intelligence"
  - "creator search"
version: 1.2
author: ROK Agency
---

# Intel Scout

Automated content discovery for the intelligence briefing system.

## Usage

```
/intel-briefing:intel-scout                      # Run full discovery scan
/intel-briefing:intel-scout --creators-only      # Only search watched creators
/intel-briefing:intel-scout --topics-only        # Only search briefing topics
/intel-briefing:intel-scout review               # Review pending recommendations
/intel-briefing:intel-scout approve <id>         # Approve recommendation for ingestion
/intel-briefing:intel-scout approve all          # Approve all above threshold
/intel-briefing:intel-scout reject <id>          # Reject recommendation
/intel-briefing:intel-scout ingest               # Ingest all approved recommendations
```

## When to Use

- Daily intelligence gathering routine
- After adding new creators to watch list
- When briefing topics change and new sources are needed
- To find content relevant to active predictions
