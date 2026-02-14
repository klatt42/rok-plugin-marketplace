---
name: recommendation-list
description: |
  Recall and display the most recent vehicle recommendation results.
  No new research performed. Supports filtering by tier (TOP_PICK,
  RECOMMENDED, CONSIDER, PASS).
triggers:
  - "recommendation list"
  - "recall vehicles"
  - "last recommendations"
  - "vehicle results"
  - "view recommendations"
version: 1.2
author: ROK Agency
---

# Recommendation List

Recall and display the most recent vehicle recommendation results.

## Usage

```
/vehicle-recommender:recommendation-list            # Show full list
/vehicle-recommender:recommendation-list --tier=TOP_PICK
```

## When to Use

- When you need to invoke /vehicle-recommender:recommendation-list
- When the user's request matches the trigger keywords above
