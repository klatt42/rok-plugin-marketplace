---
name: estate-status
description: |
  Quick read-only status check of the most recent digital estate snapshot.
  Shows estate health, critical items count, monthly burn, and last snapshot
  date without running any agents or scanning any sources.
triggers:
  - "estate status"
  - "estate health"
  - "snapshot status"
  - "last snapshot"
version: 1.0
author: ROK Agency
---

# Estate Status

Quick read-only status from the latest estate snapshot.

## Usage

```
/rok-digital-estate:estate-status            # Show latest snapshot summary
/rok-digital-estate:estate-status section:2  # Show Bus Factor Dashboard only
/rok-digital-estate:estate-status section:6  # Show Subscriptions & Costs only
```

## When to Use

- Quick check of estate health without regenerating
- Reviewing a specific section from the last snapshot
- Checking when the last snapshot was generated
