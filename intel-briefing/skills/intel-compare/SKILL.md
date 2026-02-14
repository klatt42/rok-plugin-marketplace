---
name: intel-compare
description: |
  Source comparison for the intel-briefing system. Compare prediction accuracy
  and analytical views between different content sources and authors. Reveals
  which sources are most reliable by category and tracks agreement/disagreement.
triggers:
  - "intel compare"
  - "source comparison"
  - "compare sources"
  - "compare accuracy"
  - "source reliability"
version: 1.2
author: ROK Agency
---

# Intel Compare

Compare prediction accuracy and analytical views between sources.

## Usage

```
/intel-briefing:intel-compare                              # List all sources
/intel-briefing:intel-compare sources:"Andrei Jikh,Ray Dalio"
/intel-briefing:intel-compare sources:"Andrei Jikh,Ray Dalio" category:financial
```

## When to Use

- Evaluating which sources are most accurate in a category
- Comparing contrasting viewpoints between analysts
- Deciding which sources to prioritize for ingestion
