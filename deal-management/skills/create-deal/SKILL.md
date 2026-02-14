---
name: create-deal
description: |
  Add a new deal to a sales pipeline. Gathers required information including
  pipeline, title, company, contact, value, probability, and expected
  close date.
triggers:
  - "create deal"
  - "new deal"
  - "add deal"
  - "start deal"
  - "log deal"
version: 1.2
author: ROK Agency
---

# Create Deal

Add a new deal to a sales pipeline. Gathers required information including

## Usage

```
/deal-management:create-deal                        # Interactive mode
/deal-management:create-deal title:"Acme Corp" value:50000
```

## When to Use

- When you need to invoke /deal-management:create-deal
- When the user's request matches the trigger keywords above
