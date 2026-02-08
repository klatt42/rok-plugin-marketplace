---
name: deal-scoring
description: |
  Deal scoring methodology for evaluating pipeline opportunities.
  Weighted composite scoring across value, probability, fit, urgency,
  and engagement factors. Includes grade thresholds (A-F), calibration
  guidance, and scoring adjustment patterns for different pipeline types.
triggers:
  - "score deal"
  - "deal quality"
  - "deal grade"
  - "rate deal"
  - "evaluate deal"
  - "deal assessment"
  - "prioritize deals"
version: 1.0
author: ROK Agency
---

# Deal Scoring Methodology

## Composite Score Formula

```
Score = (Value * 0.25) + (Probability * 0.20) + (Fit * 0.30) + (Urgency * 0.15) + (Engagement * 0.10)
```

Each factor is scored 0-100, then weighted.

## Factor Definitions

### Value (25%)
Measures deal dollar amount relative to pipeline context.

| Deal Value vs. Average | Score |
|------------------------|-------|
| 3x+ above average | 100 |
| 2x above average | 90 |
| At or above average | 75 |
| Below average | 50 |
| Significantly below | 25 |
| No value assigned | 10 |

### Probability (20%)
Stated win probability, cross-validated against stage position.

| Probability | Expected Stage | Score If Aligned | Score If Misaligned |
|-------------|---------------|-----------------|---------------------|
| 80-100% | Negotiation/Close | 90-100 | 60 (over-confident) |
| 60-79% | Proposal | 75-89 | 65 |
| 40-59% | Qualified | 60-74 | 55 |
| 20-39% | Lead | 45-59 | 40 |
| 0-19% | Any early stage | 30-44 | 30 |

### Fit (30%) — Heaviest Weight
Evaluates how well the opportunity matches your business.

| Signal | Points |
|--------|--------|
| Decision maker identified and engaged | +25 |
| Clear stated need matching your offering | +25 |
| Budget confirmed or likely | +20 |
| Company in target segment | +15 |
| No known competition | +15 |
| Referral or warm introduction | +10 |
| Previous relationship | +10 |

Subtract: Single-threaded (-15), unknown budget (-10), strong competition (-10)

### Urgency (15%)
Timeline pressure and compelling events.

| Signal | Score Boost |
|--------|------------|
| Hard deadline (RFP, contract end, event) | +30 |
| Expected close within 30 days | +25 |
| Expected close within 60 days | +15 |
| Stated urgency from contact | +20 |
| Budget cycle alignment | +10 |
| No timeline pressure | 0 |
| Past expected close date | -20 |
| No expected close date set | -10 |

### Engagement (10%)
Activity frequency and deal momentum.

| Activity Pattern | Score |
|-----------------|-------|
| Multiple updates this week | 90-100 |
| Update within past 3 days | 75-89 |
| Update within past 7 days | 60-74 |
| Update within past 14 days | 40-59 |
| No update in 14-30 days | 20-39 |
| No update in 30+ days | 0-19 |

## Grade Thresholds

| Grade | Score | Action |
|-------|-------|--------|
| **A** | 85-100 | Prioritize — close this deal |
| **B** | 70-84 | Active — solid deal, keep pushing |
| **C** | 55-69 | Monitor — improve weak factors |
| **D** | 40-54 | At Risk — intervene or deprioritize |
| **F** | 0-39 | Review — likely remove from pipeline |

## Calibration by Pipeline Type

### Sales Pipeline
Standard weights apply. Value and fit are primary drivers.

### Partnership Pipeline
Adjust weights: Fit (40%), Engagement (20%), Value (15%), Urgency (10%), Probability (15%).
Partnerships are relationship-driven — engagement and fit matter more than immediate value.

### Insurance Claim Pipeline
Adjust weights: Probability (30%), Value (25%), Urgency (25%), Fit (10%), Engagement (10%).
Claims are process-driven — probability and urgency reflect documentation completeness.

## Red Flags

Automatic score penalties:
- **No activity in 30+ days**: Cap score at 50 regardless of other factors
- **Past expected close with no update**: Cap score at 60
- **No contact identified**: Cap fit score at 30
- **Value = $0 with no notes**: Cap value score at 10
