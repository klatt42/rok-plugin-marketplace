name: opportunity-scoring
description: |
  Composite scoring rubric for business idea discovery. Profile fit (45%)
  plus opportunity signal (55%) with tier assignments and intersection
  multipliers. Used by the shortlist-ranker agent and scan mode scoring.

## Opportunity Scoring Methodology

### Composite Formula

```
base_composite = (profile_fit * 0.45) + (market_demand * 0.30) + (competitive_durability * 0.25)
ecosystem_modifier = 1 + (ecosystem_score / 500)  # Range: 1.0x to 1.2x
composite = min(100, base_composite * ecosystem_modifier)
# Backward compat: opportunity_signal = round((market_demand + competitive_durability) / 2)
```

For cross-pollinator intersections (applied after ecosystem modifier):
```
adjusted = min(100, composite * intersection_multiplier)
```
- 2-signal intersection: multiplier = 1.2x
- 3-signal intersection: multiplier = 1.5x

### Ecosystem Score (0-100)

Evaluates how well an idea compounds with other tools in the same niche:

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Data generation value | 30% | Core data generator (CRM data feeds analytics) | Some shared data possible | Completely isolated tool |
| Wedge product potential | 25% | Natural entry point to broader suite | Standalone but linkable | Dead end, no expansion path |
| Shared infrastructure | 25% | Deep integration (shared accounts, data layer) | Light API touch points | No shared infrastructure |
| Natural adjacency | 20% | Always bundled in mature ecosystems | Sometimes co-purchased | Unrelated to other tools |

### Profile Fit Score (0-100)

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Build complexity | 25% | Weekend project, single dev | 2-4 week MVP | Needs a team, months of work |
| Tech stack match | 20% | Next.js + Supabase + AI APIs | Familiar patterns, some new tech | Entirely unfamiliar stack |
| Domain advantage | 20% | Home services / restoration / SMB core | Adjacent industry knowledge | Zero relevant experience |
| Picks-and-shovels | 20% | Pure B2B tooling for operators | Mixed B2B/consumer | Pure consumer app |
| Exclusion check | 15% | No exclusions hit | Borderline (e.g., has e-commerce adjacent features) | Direct exclusion hit |

### Market Demand Score (0-100) — How badly do users want this?

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Pain severity & reach | 35% | Affects millions, daily pain, no workaround | Affects thousands, weekly pain, poor workarounds | Minor annoyance, few affected |
| Pain evidence quality | 30% | 10+ complaints with URLs, active threads | 2-3 signals, some dated | No evidence found |
| Market size / TAM estimate | 20% | Clear >$100M TAM, estimate grounded in evidence | $10-100M TAM, rough estimate | Tiny niche (<$1M) or insufficient data |
| Monetization clarity | 15% | Obvious SaaS subscription model | Could charge, model unclear | No clear monetization |

### Competitive Durability Score (0-100) — How hard is it to replicate?

| Factor | Weight | 100 | 50 | 0 |
|--------|--------|-----|----|----|
| Competition gap | 30% | White space, no direct competitor | 1-2 weak competitors | Saturated, 5+ strong players |
| Moat type | 30% | Strong multi-layer moat (data + switching costs) | Single moat layer | Speed-to-market only |
| Time to commoditization | 25% | 2+ years before market catches up | 6-12 months | Already commoditized |
| Platform dependency risk | 15% | Platform-independent SaaS | Moderate API dependency | Fully dependent on one platform's DOM |

Backward compatibility: `opportunity_signal = round((market_demand + competitive_durability) / 2)`

### Tier Assignments

| Composite | Tier | Action |
|-----------|------|--------|
| >= 80 | HOT | Analyze immediately with /analyze-idea |
| 65-79 | WARM | Worth a quick analysis |
| 50-64 | WATCH | Monitor, revisit with different angle |
| < 50 | PASS | Below the bar, included for completeness |

### Reference Documents

Load `references/fit-scoring-rubric.md` for detailed scoring examples and edge cases.
