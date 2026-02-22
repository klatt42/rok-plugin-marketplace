---
name: urgency-scoring
description: |
  Urgency tier definitions for the digital estate Bus Factor Dashboard.
  Four tiers (CRITICAL, ATTENTION, MONITOR, STABLE) with day thresholds,
  color codes, and criteria for domain expiry, subscription renewals,
  SSL certificates, client deliverables, and stale deployments.
triggers:
  - "urgency scoring"
  - "urgency tiers"
  - "bus factor tiers"
  - "critical items"
  - "estate urgency"
version: 1.0
author: ROK Agency
---

# Urgency Scoring

Tier definitions for the Bus Factor Dashboard.

## Tiers

| Tier | Days | Color | Hex | Criteria |
|------|------|-------|-----|----------|
| CRITICAL | <=30 | Red | #DC2626 | Domain expiring, subscription auto-renew off, active client deliverable, SSL expiring |
| ATTENTION | <=60 | Orange | #D97706 | Subscription renewal approaching, stale deployment with custom domain, unpushed changes |
| MONITOR | <=90 | Yellow | #EAB308 | Dormant projects with live domains, unused services still billing |
| STABLE | >90 | Green | #059669 | Auto-renewing, no dependencies, archived/complete |

## Scoring Rules

- Items with `auto_renew: false` automatically bump up one tier
- Active client deliverables are always CRITICAL regardless of timeline
- SSL expiry within 30 days is always CRITICAL
- Unpushed git changes on active projects are ATTENTION

See full command documentation: `commands/generate-snapshot.md`
