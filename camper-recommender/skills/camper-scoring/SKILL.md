name: camper-scoring
description: |
  Dual scoring system for camper/RV recommendations. Fit Score (55%) measures
  how well a camper matches the user's stated requirements. Market Score (45%)
  measures objective build quality and value. Tier assignments and composite ranking.
  Used by the recommendation-ranker agent.

## Camper/RV Scoring Methodology

### Dual Scoring System

Unlike single-score systems, camper recommendations use TWO independent scores:

**Fit Score (55% of composite)** — Personalized to the user's interview answers. A bunkhouse travel trailer might score 95 Fit for a family of 6 and 20 Fit for a retired couple. Same camper, different users.

**Market Score (45% of composite)** — Objective camper quality independent of user preferences. Build quality, TCO, resale value, and feature value measured against type averages.

### Composite Formula

```
composite = (fit_score * 0.55) + (market_score * 0.45)
```

### Fit Score (0-100)

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Requirements match | 30% | All must-haves met as standard (slides, bath type, capacity, off-grid) | Most met, some require upgrades | Misses critical must-haves |
| Budget alignment | 25% | Recommended floorplan under budget | At budget ceiling | Significantly over budget |
| Priority alignment | 25% | Excels in all stated priorities (build quality, weight, resale, livability) | Average in priority areas | Weak in what user cares about |
| Lifestyle fit | 20% | Perfect for stated use (weekend vs full-time, family vs couple, tow vehicle compatible) | Adequate for use case | Wrong camper type entirely |

### Market Score (0-100)

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Build quality | 30% | Premium brand, excellent construction (Airstream, Oliver, Lance) | Average build quality (Jayco, Keystone mid-line) | Known quality issues, many warranty claims |
| Value/TCO | 25% | Lowest 5yr TCO in type (incl. storage, maintenance, insurance, depreciation) | Average TCO | Highest TCO in type |
| Resale/depreciation | 20% | Best retention in class (Airstream 60%+ at 5yr) | Average retention (45-55% at 5yr) | Worst retention (<40% at 5yr) |
| Feature value | 15% | Best features-per-dollar in class | Average feature value | Poor value, competitors offer more |
| Market timing | 10% | Show season, clearance pricing, dealer incentives | Normal market conditions | Above MSRP, limited inventory |

### Tier Assignments

| Composite | Tier | Meaning | Action |
|-----------|------|---------|--------|
| >= 85 | TOP_PICK | Strong recommendation | Primary consideration |
| 70-84 | RECOMMENDED | Good option, minor trade-offs | Worth visiting dealer |
| 55-69 | CONSIDER | Notable compromises | Look at if top picks don't work out |
| < 55 | PASS | Doesn't fit well enough | Included for completeness |

### RV-Specific Scoring Notes

- **Tow vehicle compatibility is SAFETY-CRITICAL**: If GVWR exceeds tow vehicle rating, Requirements Match is capped at 25 regardless of other factors.
- **RV depreciation is steeper than vehicles**: A 5-year-old RV may retain only 40-60% of value vs 60-75% for vehicles. Brand matters enormously.
- **Build quality varies more in RVs than vehicles**: The difference between a premium and entry-level RV brand is much larger than between premium and economy cars.
- **Storage costs are unique to RVs**: This is a $1,200-$4,200/year cost that has no vehicle equivalent.

### Reference Documents

Load `references/scoring-rubric.md` for worked scoring examples and edge cases.
