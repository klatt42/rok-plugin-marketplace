---
name: intel-alert
description: |
  Topic alert management for the intel-briefing system. Create and manage alerts
  that trigger when new ingested claims match specified topics or categories.
  Useful for monitoring specific themes across all intelligence sources.
triggers:
  - "intel alert"
  - "topic alert"
  - "watch topic"
  - "alert management"
  - "claim alert"
version: 1.2
author: ROK Agency
---

# Intel Alert

Create and manage topic alerts for intelligence monitoring.

## Usage

```
/intel-briefing:intel-alert                       # List active alerts
/intel-briefing:intel-alert add:"Bitcoin ETF" category:financial
/intel-briefing:intel-alert add:"AI job displacement" category:labor
/intel-briefing:intel-alert remove:id             # Deactivate alert
/intel-briefing:intel-alert clear                 # Remove all alerts
```

## When to Use

- Setting up monitoring for specific financial or geopolitical topics
- Tracking emerging themes across ingested documents
- Managing which topics trigger notifications during ingestion
