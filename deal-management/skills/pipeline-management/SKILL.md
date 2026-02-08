---
name: pipeline-management
description: |
  Pipeline design, management, and forecasting methodology.
  Covers pipeline template design, stage naming conventions,
  velocity benchmarks, forecasting methods (weighted, time-decay,
  historical), and pipeline health indicators. Applicable to sales,
  partnerships, insurance claims, and custom business pipelines.
triggers:
  - "pipeline design"
  - "pipeline template"
  - "pipeline stages"
  - "forecast deals"
  - "pipeline health"
  - "pipeline management"
  - "pipeline velocity"
  - "deal pipeline"
version: 1.0
author: ROK Agency
---

# Pipeline Management Methodology

## Pipeline Design Principles

### Stage Design Rules

1. **3-7 stages per pipeline** — fewer than 3 provides no visibility; more than 7 creates drag
2. **Clear entry criteria** — define what must be true for a deal to enter each stage
3. **Verb-based names for action stages** — "qualifying" not "qualified" (indicates work happening)
4. **Noun-based names for state stages** — "proposal" not "proposing" (indicates a deliverable)
5. **Exit criteria match next stage's entry** — no gaps between stages
6. **First stage is low-friction** — easy to add deals, don't over-qualify at entry
7. **Last stage is definitive** — closed means closed (won or lost)

### Default Pipeline Templates

#### General Sales
```
lead -> qualified -> proposal -> negotiation -> closed
```
| Stage | Entry Criteria | Exit Criteria |
|-------|---------------|---------------|
| lead | Opportunity identified | Need and budget confirmed |
| qualified | BANT confirmed | Proposal requested |
| proposal | Proposal sent | Terms discussed |
| negotiation | Active pricing/terms discussion | Agreement reached |
| closed | Signed or declined | — |

#### Partnership
```
identified -> researched -> outreach -> connected -> agreement -> active
```
Longer pipeline reflects relationship-building nature. Partnerships require more nurturing stages.

#### Insurance Claim
```
filed -> documented -> review -> negotiation -> settlement -> closed
```
Process-driven pipeline. Stage transitions often depend on external parties (carriers, adjusters).

### Custom Pipeline Guidelines

When creating a custom pipeline:
1. Map your actual process — don't force-fit a template
2. Identify where deals stall most — create stages around those transitions
3. Each stage should take roughly similar time — split long stages, merge quick ones
4. Name stages from the customer's perspective when possible

## Velocity Benchmarks

### Sales Pipeline
| Stage | Target Days | Warning Threshold |
|-------|-------------|-------------------|
| lead | 3-5 | >10 days |
| qualified | 5-10 | >15 days |
| proposal | 3-7 | >14 days |
| negotiation | 5-14 | >21 days |
| Total cycle | 20-40 days | >60 days |

### Partnership Pipeline
| Stage | Target Days | Warning Threshold |
|-------|-------------|-------------------|
| identified | 1-3 | >7 days |
| researched | 3-7 | >14 days |
| outreach | 7-14 | >21 days |
| connected | 14-30 | >45 days |
| agreement | 14-30 | >45 days |
| Total cycle | 45-90 days | >120 days |

### Insurance Claim Pipeline
| Stage | Target Days | Warning Threshold |
|-------|-------------|-------------------|
| filed | 1-3 | >7 days |
| documented | 3-10 | >14 days |
| review | 7-21 | >30 days |
| negotiation | 7-14 | >21 days |
| settlement | 3-7 | >14 days |
| Total cycle | 25-60 days | >90 days |

## Forecasting Methods

### 1. Weighted Pipeline (Default)
```
Forecast = SUM(deal_value * probability / 100)
```
Simple, works well for pipelines with calibrated probabilities. Best for 1-3 month forecasts.

### 2. Stage-Based Probability
Override individual deal probabilities with historical stage win rates:

| Stage | Typical Win Rate |
|-------|-----------------|
| lead | 10-15% |
| qualified | 25-35% |
| proposal | 40-55% |
| negotiation | 60-75% |

Use when: Individual probability estimates are unreliable or inconsistent.

### 3. Time-Decay
```
Forecast = SUM(deal_value * probability * decay_factor)
decay_factor = 1.0 - (days_in_stage / max_expected_days) * 0.5
```
Deals that sit in a stage too long get progressively discounted. Use when: Pipeline has stale deals inflating forecast.

### 4. Historical Conversion
```
Forecast = deals_in_stage * historical_conversion_rate * avg_deal_value
```
Uses past performance to predict future outcomes. Requires 50+ historical deals for reliability.

## Pipeline Health Indicators

### Healthy Pipeline Checklist

| Indicator | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| Win Rate | >30% | 15-30% | <15% |
| Avg Cycle Time | Under benchmark | 1-2x benchmark | >2x benchmark |
| Stalled Deals | <10% | 10-25% | >25% |
| Pipeline Coverage | 3x+ target | 2-3x target | <2x target |
| Stage Balance | Funnel shape | Flat/uneven | Inverted funnel |
| Activity Rate | Daily updates | Weekly updates | Monthly or less |
| Close Date Accuracy | Within 2 weeks | Within 1 month | Frequently missed |

### Pipeline Shape

Healthy pipeline = funnel (more deals at top, fewer at bottom):
```
lead:         ========== (many)
qualified:    =======    (fewer)
proposal:     =====      (fewer still)
negotiation:  ===        (few)
closed:       ==         (some)
```

Unhealthy patterns:
- **Diamond**: Bulge in middle stages = qualification too loose, not closing
- **Inverted funnel**: More in late stages = not feeding pipeline at top
- **Hourglass**: Gaps in middle = deals skipping stages or getting stuck

## Pipeline Review Cadence

| Review Type | Frequency | Focus |
|-------------|-----------|-------|
| Quick scan | Daily | New deals, stage movements, stalled alerts |
| Pipeline review | Weekly | Stage balance, forecast update, stuck deals |
| Analytics deep-dive | Monthly | Win rate trends, velocity, coverage ratio |
| Pipeline cleanup | Quarterly | Remove stale deals, recalibrate probabilities |
