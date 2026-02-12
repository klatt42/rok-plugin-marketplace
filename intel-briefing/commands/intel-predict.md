# /intel-predict - Manage Predictions

Add, review, score, and track predictions with accuracy measurement. Predictions are forward-looking forecasts extracted from documents or added manually, tracked over time for scoring against actual outcomes.

## Usage

```
/intel-briefing:intel-predict                                       # Show pending predictions
/intel-briefing:intel-predict add:"prediction text" category:financial timeframe:6mo confidence:0.7
/intel-briefing:intel-predict review                                # Review predictions due for scoring
/intel-briefing:intel-predict score                                 # Score a specific prediction outcome
/intel-briefing:intel-predict accuracy                              # Show accuracy statistics
/intel-briefing:intel-predict list                                  # List all predictions with filters
/intel-briefing:intel-predict list category:geopolitical outcome:pending
```

### Parameters
- **add** - Prediction text to add manually
- **category** - `financial`, `geopolitical`, `technology`, `economic`, `other`
- **timeframe** - `30d`, `90d`, `6mo`, `1y`, `5y`, `indefinite`
- **confidence** - 0.0 to 1.0 (initial confidence score)
- **review** - Show predictions due for scoring (target_date <= today)
- **score** - Interactive scoring of a specific prediction
- **accuracy** - Show accuracy report with Brier scores
- **list** - List predictions with optional filters
- **outcome** - Filter by outcome status: `pending`, `correct`, `partially_correct`, `incorrect`, `indeterminate`

Initial request: $ARGUMENTS

## Execution Steps

### Mode: Add New Prediction (if "add:" is present)

1. Parse arguments:
   - `add:` (required) - The prediction text
   - `category:` (required, prompt if missing) - One of: financial, geopolitical, technology, economic, other
   - `timeframe:` (required, prompt if missing) - One of: 30d, 90d, 6mo, 1y, 5y, indefinite
   - `confidence:` (optional, default 0.5) - 0.0 to 1.0
   - `subcategory:` (optional) - More specific tag

2. Calculate `target_date` from timeframe:
   - `30d` = today + 30 days
   - `90d` = today + 90 days
   - `6mo` = today + 180 days
   - `1y` = today + 365 days
   - `5y` = today + 1825 days
   - `indefinite` = null

3. Store in `rok_intel_predictions`:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
     -H "Content-Type: application/json" \
     -H "Prefer: return=representation" \
     -d '{
       "prediction_text": "[prediction]",
       "category": "[category]",
       "subcategory": "[subcategory or null]",
       "timeframe": "[timeframe]",
       "target_date": "[calculated date or null]",
       "initial_confidence": [confidence],
       "current_confidence": [confidence],
       "outcome": "pending",
       "source_author": "manual",
       "tags": []
     }'
   ```

4. Display confirmation:
   ```
   PREDICTION ADDED
   ID: [uuid]
   Prediction: [text]
   Category: [category]
   Confidence: [score]
   Target Date: [date] ([timeframe])
   Status: Pending
   ```

### Mode: Review Due Predictions (if "review" or no args)

1. Query predictions where target_date <= today AND outcome = 'pending':
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?target_date=lte.$(date +%Y-%m-%d)&outcome=eq.pending&order=target_date.asc&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. If no predictions are due:
   ```
   No predictions currently due for review.

   Next predictions due:
   [Query and show next 5 upcoming predictions with target dates]

   Total pending: [N]
   ```

3. If predictions are due, display each one:
   ```
   PREDICTIONS DUE FOR REVIEW ([N] total)
   =========================================

   [1] [prediction_text]
       Category: [category] | Source: [source_author]
       Confidence: [initial_confidence] | Target: [target_date]
       Age: [days since created] days
       Related Document: [title if linked]

   [2] [prediction_text]
       ...
   ```

4. For each prediction, prompt the user:
   ```
   Score prediction [N]: correct / partially_correct / incorrect / indeterminate / skip
   Notes (optional):
   ```

5. For each scored prediction, update in Supabase:
   ```bash
   curl -s -X PATCH "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?id=eq.${PRED_ID}" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
     -H "Content-Type: application/json" \
     -d '{
       "outcome": "[outcome]",
       "outcome_notes": "[notes]",
       "outcome_date": "[today]",
       "updated_at": "[now]"
     }'
   ```

6. If the prediction has a linked source_author, update that source's prediction_accuracy in `rok_intel_sources` by recalculating from all evaluated predictions by that author.

7. After all reviews, display summary:
   ```
   REVIEW COMPLETE
   Scored: [N] | Skipped: [N]
   Correct: [n] | Partial: [n] | Incorrect: [n] | Indeterminate: [n]
   ```

### Mode: Score Specific Prediction (if "score")

1. Query all pending predictions:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?outcome=eq.pending&order=target_date.asc&select=id,prediction_text,category,target_date,initial_confidence,source_author" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Display numbered list:
   ```
   PENDING PREDICTIONS
   [1] [prediction_text] (category | target: [date] | confidence: [score])
   [2] [prediction_text] ...
   ...

   Select prediction to score (number):
   ```

3. After user selects, present scoring options:
   ```
   Scoring: "[prediction_text]"

   Options:
     correct (1.0)           - Prediction was accurate
     partially_correct (0.5) - Partially accurate or directionally correct
     incorrect (0.0)         - Prediction was wrong
     indeterminate           - Cannot be evaluated (excluded from accuracy)

   Score:
   Notes:
   ```

4. Update the prediction record (same PATCH as in review mode)

### Mode: Accuracy Report (if "accuracy")

1. Query all evaluated predictions (outcome != 'pending'):
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?outcome=neq.pending&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Calculate metrics (exclude 'indeterminate' from accuracy calculations):
   - **Overall accuracy rate**: (correct + 0.5 * partially_correct) / total_evaluated
   - **Brier score**: (1/N) * SUM((confidence - outcome_score)^2) where correct=1.0, partial=0.5, incorrect=0.0
   - **Accuracy by category**: Group and calculate per category
   - **Accuracy by source**: Group by source_author and calculate per source

3. Display report:
   ```
   =========================================
   PREDICTION ACCURACY REPORT
   =========================================

   Overall Performance
   -------------------
   Total Predictions: [N]
   Evaluated: [N] (Pending: [N])
   Correct: [N] | Partially Correct: [N] | Incorrect: [N] | Indeterminate: [N]
   Accuracy Rate: [X]%
   Brier Score: [X.XXXX] (lower is better; 0 = perfect, 0.25 = random)

   By Category
   -----------
   | Category      | Evaluated | Correct | Partial | Incorrect | Accuracy | Brier  |
   |---------------|-----------|---------|---------|-----------|----------|--------|
   | Financial     | [n]       | [n]     | [n]     | [n]       | [X]%     | [X.XX] |
   | Geopolitical  | [n]       | [n]     | [n]     | [n]       | [X]%     | [X.XX] |
   | ...           |           |         |         |           |          |        |

   By Source
   ---------
   | Source         | Predictions | Correct | Accuracy | Trust Tier |
   |----------------|------------|---------|----------|------------|
   | [author]       | [n]        | [n]     | [X]%     | [tier]     |
   | ...            |            |         |          |            |

   =========================================

   NEXT STEPS:
     /intel-briefing:intel-predict review          # Score pending predictions
     /intel-briefing:intel-export accuracy          # Export this report
   ```

4. Offer export: "Export accuracy report? (yes/no)"
   If yes, trigger `/intel-briefing:intel-export accuracy`

### Mode: List Predictions (if "list")

1. Build query from filters (category, outcome):
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?[filters]&order=created_at.desc&limit=50&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Display formatted list with all prediction details

## Important Rules

- **Brier score** is only calculated when 5+ evaluated predictions exist. Below that threshold, display "Insufficient data for Brier score (need 5+ evaluated predictions)"
- **Confidence decay**: When displaying predictions pending for more than 90 days past their target date, flag them with a note: "OVERDUE: [X] days past target -- consider scoring or marking indeterminate"
- Always show prediction age (days since created) and source when reviewing
- When scoring, always capture outcome_notes -- they are valuable for future calibration
- Indeterminate outcomes are excluded from accuracy calculations but tracked for reference
- After scoring predictions, offer to refresh the master briefing if 3+ predictions were just scored
- Manual predictions (added via "add:") have source_author = "manual"
