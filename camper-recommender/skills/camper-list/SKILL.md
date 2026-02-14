---
name: camper-list
description: |
  Recall and display the most recent camper/RV recommendation results.
  No new research performed. Supports filtering by tier (TOP_PICK,
  RECOMMENDED, CONSIDER, PASS).
triggers:
  - "camper list"
  - "recall campers"
  - "last recommendations"
  - "camper results"
  - "view recommendations"
version: 1.2
author: ROK Agency
---

# Camper List

Recall and display the most recent camper/RV recommendation results.

## Usage

```
/camper-recommender:camper-list                     # Show full list
/camper-recommender:camper-list --tier=TOP_PICK     # Filter by tier
```

## When to Use

- When you need to invoke /camper-recommender:camper-list
- When the user's request matches the trigger keywords above
