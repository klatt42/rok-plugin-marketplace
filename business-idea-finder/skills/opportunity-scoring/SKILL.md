name: opportunity-scoring
description: |
  Composite scoring rubric for business idea discovery. Profile fit (45%)
  plus opportunity signal (55%) with tier assignments and intersection
  multipliers. Used by the shortlist-ranker agent and scan mode scoring.

## Opportunity Scoring Methodology

### Composite Formula

```
composite = (profile_fit * 0.45) + (opportunity_signal * 0.55)
```

For cross-pollinator intersections:
```
adjusted = min(100, composite * intersection_multiplier)
```
- 2-signal intersection: multiplier = 1.2x
- 3-signal intersection: multiplier = 1.5x

### Profile Fit Score (0-100)

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Build complexity | 25% | Weekend project, single dev | 2-4 week MVP | Needs a team, months of work |
| Tech stack match | 20% | Next.js + Supabase + AI APIs | Familiar patterns, some new tech | Entirely unfamiliar stack |
| Domain advantage | 20% | Home services / restoration / SMB core | Adjacent industry knowledge | Zero relevant experience |
| Picks-and-shovels | 20% | Pure B2B tooling for operators | Mixed B2B/consumer | Pure consumer app |
| Exclusion check | 15% | No exclusions hit | Borderline (e.g., has e-commerce adjacent features) | Direct exclusion hit |

### Opportunity Signal Score (0-100)

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Pain severity & reach | 25% | Affects millions, daily pain, no workaround | Affects thousands, weekly pain, poor workarounds | Minor annoyance, few affected |
| Pain evidence quality | 20% | 10+ complaints with URLs, active threads | 2-3 signals, some dated | No evidence found |
| Competition gap | 20% | White space, no direct competitor | 1-2 weak competitors | Saturated, 5+ strong players |
| Arbitrage window | 15% | Just became possible this quarter | Possible <1 year | Been possible for years |
| Monetization clarity | 10% | Obvious SaaS subscription model | Could charge, model unclear | No clear monetization |
| Market size / TAM estimate | 10% | Clear >$100M TAM, estimate grounded in evidence | $10-100M TAM, rough estimate | Tiny niche (<$1M) or insufficient data |

### Tier Assignments

| Composite | Tier | Action |
|-----------|------|--------|
| >= 80 | HOT | Analyze immediately with /analyze-idea |
| 65-79 | WARM | Worth a quick analysis |
| 50-64 | WATCH | Monitor, revisit with different angle |
| < 50 | PASS | Below the bar, included for completeness |

### Reference Documents

Load `references/fit-scoring-rubric.md` for detailed scoring examples and edge cases.
