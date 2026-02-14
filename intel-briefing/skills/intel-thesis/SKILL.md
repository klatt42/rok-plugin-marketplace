---
name: intel-thesis
description: |
  Thesis tracking for the intel-briefing system. Track evolving narratives and
  investment theses with confidence updates over time. View confidence evolution
  timelines and archive completed or invalidated theses.
triggers:
  - "intel thesis"
  - "track thesis"
  - "investment thesis"
  - "narrative tracking"
  - "thesis confidence"
  - "evolving narrative"
version: 1.2
author: ROK Agency
---

# Intel Thesis

Track evolving narratives and investment theses with confidence updates.

## Usage

```
/intel-briefing:intel-thesis                                    # List active theses
/intel-briefing:intel-thesis add:"Fed will cut rates in H1 2026" category:financial confidence:0.6
/intel-briefing:intel-thesis update:id confidence:0.8 reason:"CPI data supports"
/intel-briefing:intel-thesis timeline:id                        # Show confidence evolution
/intel-briefing:intel-thesis archive:id                         # Archive a thesis
```

## When to Use

- Tracking a macro thesis over time with confidence adjustments
- Reviewing how thesis confidence has evolved based on new evidence
- Archiving theses that have been resolved or invalidated
