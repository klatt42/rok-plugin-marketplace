---
name: deal-analytics
description: |
  Analyze pipeline health: win rates, cycle times, stage velocity,
  bottlenecks, and value metrics. Supports filtering by pipeline and
  time period.
triggers:
  - "deal analytics"
  - "pipeline analytics"
  - "win rates"
  - "sales metrics"
  - "pipeline health"
version: 1.2
author: ROK Agency
---

# Deal Analytics

Analyze pipeline health: win rates, cycle times, stage velocity,

## Usage

```
/deal-management:deal-analytics                     # All pipelines, 30d
/deal-management:deal-analytics pipeline:general_sales period:90d
```

## When to Use

- When you need to invoke /deal-management:deal-analytics
- When the user's request matches the trigger keywords above
