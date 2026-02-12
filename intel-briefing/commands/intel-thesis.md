# Thesis Tracking

Track evolving narratives and investment theses with confidence updates over time.

## Usage

```
/intel-briefing:intel-thesis                                    # List active theses
/intel-briefing:intel-thesis add:"Fed will cut rates in H1 2026" category:financial confidence:0.6
/intel-briefing:intel-thesis update:id confidence:0.8 reason:"CPI data supports"
/intel-briefing:intel-thesis timeline:id                        # Show confidence evolution
/intel-briefing:intel-thesis archive:id                         # Archive a thesis
```

Initial request: $ARGUMENTS

## Workflow

### No args -- List Active Theses

1. Query `rok_intel_theses` where `status = 'active'`, ordered by `updated_at DESC`:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses?status=eq.active&order=updated_at.desc" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

2. For each thesis, compute the trend indicator from the last 3 entries in `confidence_history`:
   - If the last value is higher than the one before it: UP arrow
   - If the last value is lower: DOWN arrow
   - If equal or only one entry: FLAT dash

3. Count linked claims by checking `linked_claim_ids` array length.

4. Display formatted table:

```
ACTIVE THESES
=============

| # | Thesis | Category | Confidence | Trend | Claims | Updated |
|---|--------|----------|------------|-------|--------|---------|
| 1 | Fed will cut rates in H1 2026 | financial | 0.80 | ^ | 5 | 2026-02-11 |
| 2 | Dollar will weaken vs commodity currencies | financial | 0.65 | v | 3 | 2026-02-09 |
| 3 | AI regulation will accelerate in EU | technology | 0.70 | - | 1 | 2026-02-05 |

Trend: ^ = rising, v = falling, - = flat

Total active theses: 3
```

5. If no theses exist, display:

```
No active theses found.

Create one with:
  /intel-briefing:intel-thesis add:"Your thesis here" category:financial confidence:0.6
```

### "add" -- Create Thesis

1. Parse thesis text, category, and confidence from arguments
2. Validate:
   - `category` must be one of: financial, geopolitical, technology, economic, other
   - `confidence` must be between 0.0 and 1.0 (default 0.5 if not provided)
   - `thesis_text` is required

3. Build the initial confidence history entry with today's date.

4. Store in `rok_intel_theses`:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "thesis_text": "[parsed thesis text]",
    "category": "[category]",
    "initial_confidence": [confidence],
    "current_confidence": [confidence],
    "confidence_history": [{"date":"[today YYYY-MM-DD]","confidence":[confidence],"reason":"Initial thesis"}],
    "linked_claim_ids": [],
    "status": "active",
    "tags": [],
    "metadata": {}
  }'
```

5. Display confirmation:

```
Thesis Created
==============
ID:         [uuid]
Thesis:     [thesis text]
Category:   [category]
Confidence: [confidence]
Status:     active

Update confidence as new evidence emerges:
  /intel-briefing:intel-thesis update:[uuid] confidence:0.8 reason:"New evidence"
```

### "update" -- Update Confidence

1. Parse thesis ID, new confidence, and reason from arguments
2. Validate:
   - `confidence` must be between 0.0 and 1.0
   - `reason` is required (refuse update without a reason)

3. Fetch current thesis to get existing `confidence_history`:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses?id=eq.[uuid]&select=*" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

4. Append the new entry to the confidence_history array:

```json
{"date": "[today YYYY-MM-DD]", "confidence": [new_confidence], "reason": "[reason text]"}
```

5. Update the thesis with new `current_confidence`, updated `confidence_history`, and `updated_at`:

```bash
curl -s -X PATCH "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses?id=eq.[uuid]" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "current_confidence": [new_confidence],
    "confidence_history": [full updated array],
    "updated_at": "[ISO timestamp]"
  }'
```

6. Compute direction from previous confidence:
   - Increased: "UP (+X.XX)"
   - Decreased: "DOWN (-X.XX)"
   - Same: "UNCHANGED"

7. Display confirmation:

```
Thesis Updated
==============
Thesis:     [thesis text]
Previous:   [old confidence]
Current:    [new confidence] [direction]
Reason:     [reason text]
Updates:    [total history entries]

View full timeline:
  /intel-briefing:intel-thesis timeline:[uuid]
```

### "timeline" -- Show Confidence Evolution

1. Fetch thesis by ID:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses?id=eq.[uuid]&select=*" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

2. Also count linked claims:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?id=in.([comma-separated linked_claim_ids])&select=id" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

3. Display the full confidence timeline with ASCII chart:

```
THESIS TIMELINE
===============
Thesis:   "[thesis text]"
Category: [category] | Status: [status]
Created:  [created_at] | Last Updated: [updated_at]

Confidence History:
  [date]       [confidence]  [reason]
  2026-02-01   0.60          Initial thesis
  2026-02-05   0.55          Jobs report stronger than expected
  2026-02-08   0.65          Dovish Fed commentary
  2026-02-11   0.80          CPI data supports rate cut narrative

       +------------------------------------------+
  1.0  |                                          |
  0.8  |                                     *    |
  0.65 |                           *              |
  0.6  |  *                                       |
  0.55 |          *                                |
  0.0  |                                          |
       +------------------------------------------+
        Feb 1     Feb 5     Feb 8     Feb 11

Linked Claims: [N]
  - "[claim text snippet...]" ([category], [confidence])
  - "[claim text snippet...]" ([category], [confidence])
```

4. If thesis has no linked claims, display "Linked Claims: 0 (none yet)"

### "archive" -- Archive Thesis

1. Fetch thesis by ID:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses?id=eq.[uuid]&select=*" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

2. Display current thesis state and ask for archive reason:

```
Archive Thesis
==============
Thesis:     "[thesis text]"
Confidence: [current] (started at [initial])
Updates:    [history count]
Claims:     [linked count]

Archive as:
  1. confirmed    - Thesis proved correct
  2. invalidated  - Thesis proved wrong
  3. archived     - No longer tracking (inconclusive)

Select (1/2/3):
```

3. Update the thesis status:

```bash
curl -s -X PATCH "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses?id=eq.[uuid]" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "status": "[confirmed|invalidated|archived]",
    "updated_at": "[ISO timestamp]"
  }'
```

4. Display confirmation:

```
Thesis Archived
===============
Thesis:  "[thesis text]"
Status:  [new status]
Journey: [initial_confidence] -> [current_confidence] over [N] updates

This thesis is no longer active and will not receive auto-linked claims.
```

## Auto-Linking Logic (used during ingestion)

When new claims are ingested via `/intel-briefing:intel-ingest`:

1. Query all active theses:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses?status=eq.active" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

2. For each thesis, check if new claims share:
   - Same `category` as the thesis
   - Overlapping `subcategory` or `tags` with thesis keywords (extracted from thesis_text)

3. If a match is found, append the claim's UUID to `linked_claim_ids`:

```bash
curl -s -X PATCH "${ROK_SUPABASE_URL}/rest/v1/rok_intel_theses?id=eq.[thesis_uuid]" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"linked_claim_ids": [updated array with new claim UUID], "updated_at": "[ISO timestamp]"}'
```

4. Report auto-linked claims in the ingestion summary:

```
THESIS LINKS
=============
Thesis "Fed will cut rates in H1 2026" linked to 2 new claims:
  - "January CPI came in at 2.1%" (financial/inflation)
  - "Fed officials signal openness to rate adjustments" (financial/fed-policy)
```

## Rules

- Confidence must be between 0.0 and 1.0 -- reject values outside this range
- Confidence history is append-only -- entries are never modified or deleted retroactively
- Reason is required for every confidence update -- refuse the update without one
- Timeline display uses ASCII art for terminal compatibility (no Unicode box-drawing)
- Default confidence is 0.5 if not specified on creation
- Archived theses (any non-active status) are excluded from auto-linking
- When displaying theses, always show the trend indicator based on last 3 history entries
- Linked claim IDs are stored as a UUID array; validate that IDs exist before linking
- The `updated_at` field must be set on every modification (update, archive, auto-link)
