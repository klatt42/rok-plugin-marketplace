---
name: campaign-dashboard
description: |
  Overview of all campaigns with status, funnel metrics, and actionable flags.
  Displays campaign health at a glance with filtering by channel and status.
triggers:
  - "campaign dashboard"
  - "campaign overview"
  - "all campaigns"
  - "campaign status"
  - "campaign health"
version: 1.2
author: ROK Agency
---

# Campaign Dashboard

Overview of all campaigns with status, funnel metrics, and actionable flags.

## Usage

```
/campaign-management:campaign-dashboard             # Full dashboard
/campaign-management:campaign-dashboard channel:email status:active
```

## When to Use

- When you need to invoke /campaign-management:campaign-dashboard
- When the user's request matches the trigger keywords above
