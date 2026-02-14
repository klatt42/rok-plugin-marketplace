---
name: deal-export
description: |
  Export pipeline deals to professional Excel and PDF reports. Supports
  filtering by pipeline name and deal status (active, won, lost).
triggers:
  - "deal export"
  - "export deals"
  - "pipeline report"
  - "deal report"
  - "download deals"
version: 1.2
author: ROK Agency
---

# Deal Export

Export pipeline deals to professional Excel and PDF reports. Supports

## Usage

```
/deal-management:deal-export                        # Export active deals
/deal-management:deal-export pipeline:general_sales status:won
```

## When to Use

- When you need to invoke /deal-management:deal-export
- When the user's request matches the trigger keywords above
