---
name: generate-snapshot
description: |
  Generate a comprehensive digital estate snapshot for bus factor mitigation and
  work continuity. Scans local projects, GitHub repos, Netlify/Vercel deployments,
  ROK Supabase memory, and manual infrastructure config. Produces a 10-section
  estate document with urgency-scored items. Exports to HTML, PDF, and Markdown.
triggers:
  - "digital estate"
  - "estate snapshot"
  - "bus factor"
  - "generate snapshot"
  - "estate scan"
  - "continuity document"
version: 1.0
author: ROK Agency
---

# Generate Snapshot

Generate a comprehensive digital estate snapshot for work continuity.

## Usage

```
/rok-digital-estate:generate-snapshot                    # Full snapshot (all sources)
/rok-digital-estate:generate-snapshot refresh            # Force regeneration
/rok-digital-estate:generate-snapshot source:local       # Local projects only
/rok-digital-estate:generate-snapshot source:github      # GitHub repos only
/rok-digital-estate:generate-snapshot source:deployments # Deployments only
```

## When to Use

- Monthly estate snapshot generation
- After major project changes (new deploys, new repos, domain changes)
- Preparing a bus factor document for family continuity planning
- Auditing project/deployment/subscription status
