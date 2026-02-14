---
name: deal-forecast
description: |
  Generate a weighted revenue forecast based on deal probabilities and
  expected close dates. Configurable forecast horizon by pipeline.
triggers:
  - "deal forecast"
  - "revenue forecast"
  - "sales forecast"
  - "pipeline forecast"
  - "projected revenue"
version: 1.2
author: ROK Agency
---

# Deal Forecast

Generate a weighted revenue forecast based on deal probabilities and

## Usage

```
/deal-management:deal-forecast                      # 3-month forecast
/deal-management:deal-forecast months:6 pipeline:general_sales
```

## When to Use

- When you need to invoke /deal-management:deal-forecast
- When the user's request matches the trigger keywords above
