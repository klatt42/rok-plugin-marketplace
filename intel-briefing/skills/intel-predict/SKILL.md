---
name: intel-predict
description: |
  Prediction management and accuracy tracking. Add, review, score, and track
  predictions with Brier score accuracy measurement. Predictions are forward-looking
  forecasts extracted from documents or added manually, tracked over time.
triggers:
  - "intel predict"
  - "manage predictions"
  - "add prediction"
  - "score prediction"
  - "prediction accuracy"
  - "review predictions"
version: 1.2
author: ROK Agency
---

# Intel Predict

Manage predictions with accuracy measurement.

## Usage

```
/intel-briefing:intel-predict                                       # Show pending predictions
/intel-briefing:intel-predict add:"prediction text" category:financial timeframe:6mo confidence:0.7
/intel-briefing:intel-predict review                                # Review due predictions
/intel-briefing:intel-predict score                                 # Score an outcome
/intel-briefing:intel-predict accuracy                              # Show accuracy statistics
/intel-briefing:intel-predict list category:geopolitical outcome:pending
```

## When to Use

- Adding manual predictions to track
- Reviewing predictions that are due for scoring
- Checking prediction accuracy by source or category
