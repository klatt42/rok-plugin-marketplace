---
name: find-vehicle
description: |
  Search real vehicle inventory from major aggregator sites. Takes finder
  prompts from vehicle-recommender output or freeform search text to find
  actual listings with pricing, dealer info, and deal ratings.
triggers:
  - "find vehicle"
  - "search vehicles"
  - "vehicle inventory"
  - "car listings"
  - "vehicle search"
version: 1.2
author: ROK Agency
---

# Find Vehicle

Search real vehicle inventory from major aggregator sites. Takes finder

## Usage

```
/vehicle-finder:find-vehicle 2026 Toyota RAV4 Hybrid XLE under $38,000
/vehicle-finder:find-vehicle --from-recommendations # From last recommender run
```

## When to Use

- When you need to invoke /vehicle-finder:find-vehicle
- When the user's request matches the trigger keywords above
