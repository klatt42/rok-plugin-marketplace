---
name: medigap-scoring
description: |
  Scoring methodology for Medigap Plan G vs Plan N selection. Suitability
  scoring (0-100) with cost efficiency, risk protection, flexibility,
  priority alignment, and insurer quality factors.
triggers:
  - "medigap score"
  - "medigap scoring"
  - "plan comparison scoring"
version: 1.0
author: ROK Agency
---

# Medigap Scoring Methodology

Scoring system for ranking Plan G vs Plan N suitability based on user-specific factors.

## Reference Documents

Load on-demand:

- `references/scoring-rubric.md` — Worked examples with factor breakdowns

## Scoring Factors

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Cost efficiency | 30% | Premium savings vs out-of-pocket risk |
| Risk protection | 25% | Coverage gaps, excess charge exposure |
| Flexibility | 20% | Switching ability, birthday rule |
| Priority alignment | 15% | Match to user's stated priorities |
| Insurer quality | 10% | AM Best, NAIC, rate stability |

## Confidence Levels

- **HIGH**: Winner by >$300/year + priority alignment + 3+ premium sources
- **MEDIUM**: Winner by $100-$300/year or mixed signals
- **LOW**: Winner by <$100/year or insufficient data

## When to Use

- During recommendation synthesis phase
- When scoring Plan G vs Plan N for a specific user profile
