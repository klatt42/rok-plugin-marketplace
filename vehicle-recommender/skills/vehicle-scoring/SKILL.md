name: vehicle-scoring
description: |
  Dual scoring system for vehicle recommendations. Fit Score (55%) measures
  how well a vehicle matches the user's stated requirements. Market Score (45%)
  measures objective vehicle quality. Tier assignments and composite ranking.
  Used by the recommendation-ranker agent.

## Vehicle Scoring Methodology

### Dual Scoring System

Unlike single-score systems, vehicle recommendations use TWO independent scores:

**Fit Score (55% of composite)** — Personalized to the user's interview answers. A minivan might score 95 Fit for a family of 6 and 20 Fit for a single commuter. Same vehicle, different users.

**Market Score (45% of composite)** — Objective vehicle quality independent of user preferences. Reliability, TCO, resale value, and feature value measured against segment averages.

### Composite Formula

```
composite = (fit_score * 0.55) + (market_score * 0.45)
```

### Fit Score (0-100)

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Requirements match | 30% | All must-haves met as standard | Most met, some require options | Misses critical must-haves |
| Budget alignment | 25% | Recommended trim under budget | At budget ceiling | Significantly over budget |
| Priority alignment | 25% | Excels in all stated priorities | Average in priority areas | Weak in what user cares about |
| Lifestyle fit | 20% | Perfect for stated use case | Adequate for use case | Wrong vehicle type entirely |

### Market Score (0-100)

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Reliability | 30% | CR 5/5, no recalls, proven platform | Average ratings, minor issues | Below average, significant recalls |
| Value/TCO | 25% | Lowest 5yr TCO in segment | Average TCO | Highest TCO in segment |
| Resale/depreciation | 20% | Best 3yr residual in class (>70%) | Average residual (55-65%) | Worst residual in class (<50%) |
| Feature value | 15% | Best features-per-dollar | Average feature value | Poor value, competitors offer more |
| Market timing | 10% | Strong incentives, good inventory | Normal market conditions | Dealer markups, supply constraints |

### Tier Assignments

| Composite | Tier | Meaning | Action |
|-----------|------|---------|--------|
| >= 85 | TOP_PICK | Strong recommendation | Primary consideration |
| 70-84 | RECOMMENDED | Good option, minor trade-offs | Worth test driving |
| 55-69 | CONSIDER | Notable compromises | Test drive if top picks don't work out |
| < 55 | PASS | Doesn't fit well enough | Included for completeness |

### Reference Documents

Load `references/scoring-rubric.md` for worked scoring examples and edge cases.
