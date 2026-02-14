---
name: intel-briefing
description: |
  Generate or view the cumulative master intelligence briefing. Synthesizes all
  ingested documents into four analytical pillars: financial outlook, geopolitical
  analysis, AI & technology, and labor markets. Includes prediction tracking and
  cross-domain theme detection.
triggers:
  - "intel briefing"
  - "master briefing"
  - "intelligence report"
  - "generate briefing"
  - "briefing update"
  - "daily briefing"
version: 1.2
author: ROK Agency
---

# Intel Briefing

Generate or view the cumulative master intelligence briefing.

## Usage

```
/intel-briefing:intel-briefing                    # Show current briefing
/intel-briefing:intel-briefing refresh            # Force regeneration
/intel-briefing:intel-briefing category:financial  # Financial section only
/intel-briefing:intel-briefing category:geopolitical
/intel-briefing:intel-briefing category:technology
/intel-briefing:intel-briefing category:labor
/intel-briefing:intel-briefing since:2026-01-01
```

## When to Use

- Generating or refreshing the master intelligence briefing
- Reviewing a specific analytical section
- After ingesting new documents to see updated synthesis
