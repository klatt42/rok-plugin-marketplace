# Topic Alert Management

Create and manage topic alerts that trigger when new claims match specified topics.

## Usage

```
/intel-briefing:intel-alert                       # List active alerts
/intel-briefing:intel-alert add:"Bitcoin ETF" category:financial
/intel-briefing:intel-alert remove:id             # Deactivate alert
/intel-briefing:intel-alert clear                 # Remove all alerts
```

Initial request: $ARGUMENTS

## Workflow

### No args -- List Active Alerts

1. Query `rok_intel_alerts` where `active = true`, ordered by `created_at DESC`:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?active=eq.true&order=created_at.desc" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

2. Display formatted table:

```
ACTIVE ALERTS
=============

| # | Topic | Category | Matches | Last Matched | Created |
|---|-------|----------|---------|--------------|---------|
| 1 | Bitcoin ETF | financial | 12 | 2026-02-10 | 2026-01-15 |
| 2 | Fed rate decision | financial | 8 | 2026-02-09 | 2026-01-20 |
| 3 | China semiconductor | geopolitical | 3 | 2026-02-05 | 2026-02-01 |

Total active alerts: 3
```

3. If no alerts exist, display:

```
No active alerts found.

Create one with:
  /intel-briefing:intel-alert add:"Your topic here" category:financial
```

### "add" -- Create Alert

1. Parse topic text and optional category from arguments
2. Extract keywords from topic text (split on spaces, lowercase, remove common stop words: "the", "a", "an", "is", "of", "in", "to", "and", "or", "for")
3. Validate category if provided (must be one of: financial, geopolitical, technology, economic, market, policy, military, social, energy, other)
4. Store in `rok_intel_alerts`:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "topic": "[parsed topic text]",
    "category": "[category or null]",
    "keywords": ["keyword1", "keyword2"],
    "active": true,
    "match_count": 0,
    "metadata": {}
  }'
```

5. Display confirmation:

```
Alert Created
=============
ID:       [uuid]
Topic:    [topic text]
Category: [category or "all"]
Keywords: [keyword1, keyword2, ...]

Will notify when new claims match these keywords during ingestion.
```

### "remove" -- Deactivate Alert

1. Parse alert ID from arguments (accepts UUID or partial UUID)
2. If partial, query to find the matching alert first:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?id=like.*[partial]*&active=eq.true" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

3. Set `active = false` (soft delete):

```bash
curl -s -X PATCH "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?id=eq.[uuid]" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"active": false}'
```

4. Display confirmation:

```
Alert Deactivated
=================
Topic:   [topic text]
Matches: [match_count] total matches before deactivation

The alert will no longer trigger during ingestion.
To reactivate, create a new alert with the same topic.
```

### "clear" -- Remove All Alerts

1. First, query to show what will be deactivated:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?active=eq.true&select=id,topic,match_count" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

2. Display the list and ask for confirmation:

```
The following [N] alerts will be deactivated:
  - "Bitcoin ETF" (12 matches)
  - "Fed rate decision" (8 matches)
  - "China semiconductor" (3 matches)

Proceed? (yes/no)
```

3. On confirmation, set all active alerts to `active = false`:

```bash
curl -s -X PATCH "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?active=eq.true" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"active": false}'
```

4. Display confirmation:

```
All Alerts Cleared
==================
[N] alerts deactivated.

Create new alerts with:
  /intel-briefing:intel-alert add:"Your topic here" category:financial
```

## Alert Matching Logic (used by /intel-ingest)

During ingestion, new claims are matched against active alerts:

1. Fetch all active alerts:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?active=eq.true" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

2. For each active alert, check if the new claim's `claim_text` or `tags` array contains any of the alert's keywords (case-insensitive substring match)
3. If the alert has a `category` set, only match claims whose `category` matches
4. On match:
   - Increment `match_count` by 1
   - Update `last_matched` to current timestamp
   - Flag the claim for display in the ingestion report

```bash
curl -s -X PATCH "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?id=eq.[alert_uuid]" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"match_count": [incremented], "last_matched": "[ISO timestamp]"}'
```

5. After ingestion, display matched alerts in a summary section:

```
ALERT MATCHES
=============
[!] "Bitcoin ETF" matched 2 new claims:
    - "BlackRock Bitcoin ETF saw $500M inflows this week" (financial)
    - "SEC reviewing new Bitcoin ETF applications" (policy)
```

## Rules

- Alerts are soft-deleted (`active = false`), never hard-deleted from the database
- Keywords are always stored and matched case-insensitively
- Stop words (the, a, an, is, of, in, to, and, or, for) are stripped from keyword extraction
- Alert matching happens during ingestion, not as a separate background process
- A single claim can match multiple alerts
- `clear` always requires user confirmation before proceeding
- Category is optional -- omitting it means the alert matches across all categories
- Display match_count as 0 for newly created alerts
