---
name: find-camper
description: |
  Search real camper/RV inventory from major aggregator sites. Takes finder
  prompts from camper-recommender output or freeform search text to find
  actual listings with pricing, dealer info, and deal ratings.
triggers:
  - "find camper"
  - "search campers"
  - "camper inventory"
  - "rv listings"
  - "camper search"
version: 1.2
author: ROK Agency
---

# Find Camper

Search real camper/RV inventory from major aggregator sites. Takes finder

## Usage

```
/camper-finder:find-camper 2025 Grand Design Imagine 2500RL under $45,000
/camper-finder:find-camper --from-recommendations   # From last recommender run
```

## When to Use

- When you need to invoke /camper-finder:find-camper
- When the user's request matches the trigger keywords above
