---
name: idea-scoring
description: |
  Composite scoring methodology for plugin ideas. Three dimensions:
  Personal Utility (40%), Marketization (35%), Novelty (25%).
  Tiers: BUILD_NOW (>=80), STRONG (65-79), BACKLOG (50-64), PASS (<50).
  Used by shortlist-ranker agent and generate-ideas command.
triggers:
  - "score plugin idea"
  - "rank plugin ideas"
  - "plugin scoring rubric"
version: 1.0
author: ROK Agency
---

# Plugin Idea Scoring Methodology

## Three-Dimension Composite Score

Plugin ideas are scored across three dimensions weighted by the operator's priorities:

### 1. Personal Utility Score (40% weight)

How useful is this plugin to the operator personally?

| Factor | Weight | Criteria |
|--------|--------|----------|
| Solves a real pain | 30% | Would you use this weekly? (100=daily use, 50=monthly, 0=wouldn't use) |
| Domain expertise match | 25% | Leverages existing knowledge? (100=core domain, 50=adjacent, 0=unfamiliar) |
| Tech stack alignment | 20% | Uses Next.js/Supabase/Claude/Python/Chrome? (100=exact match, 0=unfamiliar) |
| Portfolio synergy | 25% | Extends existing plugins or fills clear gap? (100=natural extension, 50=standalone but fits, 0=orphan) |

### 2. Marketization Score (35% weight)

How sellable is this as a standalone product?

| Factor | Weight | Criteria |
|--------|--------|----------|
| Market demand signal | 30% | Evidence people want this? (100=abundant complaints/requests, 0=speculation) |
| Product pathway clarity | 25% | Clear path from plugin to product? (100=obvious SaaS/extension, 0=CLI-only forever) |
| Willingness to pay | 25% | Would target users pay? (100=saves money/time daily, 0=nice-to-have) |
| Competitive landscape | 20% | Underserved or no direct competitor? (100=white space, 0=saturated) |

### 3. Novelty Score (25% weight)

How creative and differentiated is this idea?

| Factor | Weight | Criteria |
|--------|--------|----------|
| Originality | 40% | Does this exist as a plugin anywhere? (100=first of its kind, 0=clone of existing) |
| AI-native advantage | 35% | Fundamentally better with AI? (100=impossible without AI, 0=AI is a gimmick) |
| Trend alignment | 25% | Rides an emerging wave? (100=leverages brand-new capability, 0=mature space) |

## Composite Formula

```
composite = (personal_utility * 0.40) + (marketization * 0.35) + (novelty * 0.25)
```

## Tier Assignments

| Composite | Tier | Meaning |
|-----------|------|---------|
| >= 80 | BUILD_NOW | Strong fit, clear market, build this next |
| 65-79 | STRONG | Good idea, worth a validation sprint |
| 50-64 | BACKLOG | Interesting but not urgent |
| < 50 | PASS | Doesn't fit well enough right now |

## Product Pathway Types

Each idea is assigned a primary product pathway:

| Pathway | Description |
|---------|-------------|
| `saas_app` | Web app with subscription model (Next.js + Supabase + Stripe) |
| `chrome_extension` | Browser-native tool, Chrome Web Store distribution |
| `api_service` | Expose as an API others can consume |
| `marketplace_plugin` | Publishable Claude Code plugin (stays in ecosystem) |
| `mobile_app` | Mobile-first product (React Native) |
| `hybrid` | Multiple pathways viable |

## Reference Documents

- `references/operator-profile.md` — Hardcoded user profile for fit scoring
- `references/scoring-rubric.md` — Detailed examples of high/medium/low scoring ideas
