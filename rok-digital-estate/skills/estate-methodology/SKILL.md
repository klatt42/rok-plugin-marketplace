---
name: estate-methodology
description: |
  Data collection methodology for the digital estate snapshot. Defines how
  projects are classified by activity status, how cross-referencing works
  between local projects, GitHub repos, and deployments, staleness detection
  rules, and completeness scoring for snapshot quality.
triggers:
  - "estate methodology"
  - "snapshot methodology"
  - "cross-reference"
  - "staleness rules"
  - "completeness scoring"
version: 1.0
author: ROK Agency
---

# Estate Methodology

Reference document for data collection and cross-referencing rules.

## Activity Classification

| Status | Criteria | Color |
|--------|----------|-------|
| Active | Last commit < 30 days ago | Green |
| Recent | Last commit 30-90 days ago | Blue |
| Dormant | Last commit 90-365 days ago | Yellow |
| Abandoned | Last commit > 365 days ago | Gray |

## Cross-Referencing

Three-way match: Local Path <-> GitHub Remote URL <-> Deployment Repo
- Match by git remote URL (normalize .git suffix)
- Match deployments by repo name or connected repo
- Flag orphans (exist in one source but not others)

## Completeness Scoring

| Score | Meaning |
|-------|---------|
| 100% | All 5 data sources responded with full data |
| 80% | 4 of 5 sources, or all 5 with partial data |
| 60% | 3 of 5 sources |
| < 60% | Significant data gaps - review missing_data arrays |

See full command documentation: `commands/generate-snapshot.md`
