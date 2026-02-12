---
name: prediction-tracking
description: |
  Prediction management, scoring, and accuracy measurement methodology for the
  intel-briefing plugin. Contains Brier score calculation, outcome classification
  criteria, confidence decay formulas, calibration analysis, and accuracy reporting
  formats. Load when scoring predictions or generating accuracy reports.
triggers:
  - "prediction tracking"
  - "prediction scoring"
  - "brier score"
  - "prediction accuracy"
  - "forecast tracking"
  - "outcome scoring"
version: 1.0
author: ROK Agency
---

# Prediction Tracking Skill

## When to Use This Skill

Load when adding predictions, scoring outcomes, generating accuracy reports, or reviewing prediction calibration.

## Prediction Lifecycle

```
Extracted -> Stored (pending) -> Due for Review -> Scored (outcome) -> Accuracy Calculated
```

## Timeframe Normalization

| Label | Duration | Target Date Calculation |
|-------|----------|----------------------|
| `30d` | 30 days | extraction_date + 30 days |
| `90d` | 90 days | extraction_date + 90 days |
| `6mo` | 6 months | extraction_date + 180 days |
| `1y` | 1 year | extraction_date + 365 days |
| `2y` | 2 years | extraction_date + 730 days |
| `5y` | 5 years | extraction_date + 1825 days |
| `indefinite` | No fixed date | Review annually |

## Outcome Classification

| Outcome | Criteria | Brier Value |
|---------|----------|-------------|
| `correct` | Prediction clearly occurred as stated | 1.0 |
| `partially_correct` | Core thesis correct but timing or details differ | 0.5 |
| `incorrect` | Prediction clearly did not occur | 0.0 |
| `indeterminate` | Cannot evaluate (ambiguous wording, external factors) | Excluded from scoring |

## Brier Score Calculation

```
Brier Score = (1/N) x SUM(confidence_i - outcome_i)^2

Where:
- confidence_i = initial_confidence when prediction was made
- outcome_i = 1.0 (correct), 0.5 (partial), 0.0 (incorrect)
- Lower Brier Score = better calibration
- Perfect calibration = 0.0
- Random guessing = 0.25
```

**Interpretation:**

| Brier Score | Quality |
|-------------|---------|
| 0.00-0.10 | Excellent calibration |
| 0.10-0.20 | Good calibration |
| 0.20-0.30 | Average (random-adjacent) |
| 0.30+ | Poor calibration |

## Confidence Decay

Claims and predictions lose confidence over time without revalidation:

```
decayed_confidence = current_confidence x decay_factor

Decay schedule:
- 0-30 days: No decay (1.0)
- 31-60 days: 0.95
- 61-90 days: 0.90
- 91-180 days: 0.80
- 181-365 days: 0.65
- 365+ days: 0.50
```

Revalidation resets the decay clock.

## Calibration Analysis

Track whether confidence scores match actual outcomes:

```
For each confidence bucket (0.1-0.2, 0.2-0.3, ..., 0.9-1.0):
  actual_rate = correct_outcomes / total_predictions
  expected_rate = average_confidence_in_bucket
  calibration_error = |actual_rate - expected_rate|
```

**Good calibration**: Predictions made with 70% confidence should come true ~70% of the time.

## Source Accuracy Tracking

Track prediction accuracy per source/author:

```
source_accuracy = correct_predictions / total_evaluated_predictions
```

This feeds back into source trust tier adjustments:
- accuracy > 70% -- consider upgrading trust tier
- accuracy < 30% -- consider downgrading trust tier

## Accuracy Report Format

```markdown
## Prediction Accuracy Report -- [Date]

### Overall Performance
- Total Predictions: [N]
- Evaluated: [E] | Pending: [P]
- Correct: [C] ([%]) | Partial: [Pa] ([%]) | Incorrect: [I] ([%])
- Brier Score: [X.XXXX]

### By Category
| Category | Evaluated | Correct | Partial | Incorrect | Accuracy | Brier |
|----------|-----------|---------|---------|-----------|----------|-------|

### By Source
| Source | Predictions | Correct | Accuracy | Trust Tier |
|--------|------------|---------|----------|------------|

### By Timeframe
| Timeframe | Evaluated | Accuracy | Brier |
|-----------|-----------|----------|-------|

### Calibration
| Confidence Bucket | Predictions | Actual Rate | Expected Rate | Error |
|-------------------|-------------|-------------|---------------|-------|
```
