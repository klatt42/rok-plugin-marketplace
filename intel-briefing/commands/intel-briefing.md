# /intel-briefing - Generate Master Intelligence Briefing

Generate or view the cumulative intelligence master briefing, synthesizing all ingested documents into financial forecasts, geopolitical analysis, prediction tracking, and cross-domain themes.

## Usage

```
/intel-briefing:intel-briefing                    # Show current briefing
/intel-briefing:intel-briefing refresh            # Force regeneration from all data
/intel-briefing:intel-briefing category:financial  # Focus on financial section only
/intel-briefing:intel-briefing category:geopolitical # Focus on geopolitical section only
/intel-briefing:intel-briefing category:labor        # Focus on labor section only
/intel-briefing:intel-briefing since:2026-01-01    # Only include data since date
```

### Parameters
- **refresh** - Force regeneration even if a recent briefing exists
- **category** - Focus on a single section: `financial`, `geopolitical`, `labor`
- **since** - Only consider data after this date (ISO format YYYY-MM-DD)

Initial request: $ARGUMENTS

## Execution Steps

### Phase 1: Check Current State

1. Query the latest briefing from Supabase:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_briefings?order=version.desc&limit=1&select=id,version,created_at,document_count,claim_count,prediction_count,executive_summary,full_briefing_md" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Parse the response:
   - If no briefing exists, proceed to Phase 2 to generate the inaugural briefing
   - If a briefing exists and `refresh` is NOT in $ARGUMENTS:
     - Check if briefing is recent (created_at within 24 hours)
     - If recent: display the `full_briefing_md` content and ask "This briefing is [X hours] old. Refresh with latest intelligence? (yes/no)"
     - If stale (older than 24h): note "Briefing is [X days] old" and proceed to Phase 2

3. If `refresh` IS in $ARGUMENTS, always proceed to Phase 2 regardless of age

Display:
```
BRIEFING STATUS
Latest Version: v[N] (generated [date/time])
Documents: [count] | Claims: [count] | Predictions: [count]
Status: [Current / Stale / None]
```

### Phase 2: Gather Intelligence

1. Determine the date boundary:
   - If `since:` parameter provided, use that date
   - If previous briefing exists, use its `created_at` as the boundary
   - If no previous briefing, use all data (no boundary)

2. Query new claims since the boundary:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?extraction_date=gt.${BOUNDARY_DATE}&order=extraction_date.desc&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

3. If no new claims since last briefing and not a forced refresh:
   - Display current briefing with note: "No new intelligence since [date]. Showing current briefing v[N]."
   - Stop here

4. Query additional context:
   ```bash
   # Total document count
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?select=id&limit=1" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
     -H "Prefer: count=exact" -I

   # Predictions due for review (target_date <= today, outcome = pending)
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?target_date=lte.$(date +%Y-%m-%d)&outcome=eq.pending&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

   # Active alerts
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?active=eq.true&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

   # All claims for full synthesis (for refresh or inaugural)
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?order=extraction_date.desc&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

   # Recent prediction outcomes
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?outcome=neq.pending&order=outcome_date.desc&limit=20&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

5. Get previous briefing sections (financial_section, geopolitical_section, labor_section) for delta detection context

Display:
```
INTELLIGENCE GATHERED
New Claims Since Last: [N]
Total Claims: [N]
  Financial: [n] | Geopolitical: [n] | Technology: [n] | Labor: [n] | Other: [n]
Predictions Pending: [N] | Due for Review: [N]
Active Alerts: [N]
```

### Phase 3: Specialized Analysis (Parallel Dispatch)

If `category:financial` is specified, skip geopolitical and labor. If `category:geopolitical` is specified, skip financial and labor. If `category:labor` is specified, skip financial and geopolitical. Otherwise dispatch all three.

1. Group claims by category for targeted dispatch

2. **Dispatch financial-analyst** agent (background):
   ```
   Task(
     description: "Financial synthesis for master briefing",
     prompt: "You are the financial-analyst agent. [Include agent instructions from agents/financial-analyst.md]

     FINANCIAL CLAIMS:
     [JSON array of all financial/economic/market category claims]

     PREVIOUS FINANCIAL SECTION:
     [Previous briefing's financial section text, or 'This is the inaugural briefing']

     CURRENT DATE: [today's date]

     Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

3. **Dispatch geopolitical-analyst** agent (background):
   ```
   Task(
     description: "Geopolitical synthesis for master briefing",
     prompt: "You are the geopolitical-analyst agent. [Include agent instructions from agents/geopolitical-analyst.md]

     GEOPOLITICAL CLAIMS:
     [JSON array of all geopolitical/military/policy category claims]

     PREVIOUS GEOPOLITICAL SECTION:
     [Previous briefing's geopolitical section text, or 'This is the inaugural briefing']

     CURRENT DATE: [today's date]

     Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

4. **Dispatch labor-analyst** agent (background):
   ```
   Task(
     description: "Labor synthesis for master briefing",
     prompt: "You are the labor-analyst agent. [Include agent instructions from agents/labor-analyst.md]

     LABOR CLAIMS:
     [JSON array of all labor/workforce/employment category claims]

     PREVIOUS LABOR SECTION:
     [Previous briefing's labor section text, or 'This is the inaugural briefing']

     CURRENT DATE: [today's date]

     Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

5. Collect results from all agents via TaskOutput (block: true):
   ```
   TaskOutput(task_id: "<financial_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<geopolitical_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<labor_task_id>", block: true, timeout: 120000)
   ```

Display:
```
SPECIALIZED ANALYSIS COMPLETE
Financial Section: [Ready / Skipped / Error]
Geopolitical Section: [Ready / Skipped / Error]
Labor Section: [Ready / Skipped / Error]
```

### Phase 4: Master Synthesis

1. **Dispatch briefing-synthesizer** agent with all gathered data:
   ```
   Task(
     description: "Synthesize master intelligence briefing",
     prompt: "You are the briefing-synthesizer agent. [Include agent instructions from agents/briefing-synthesizer.md]

     FINANCIAL SECTION OUTPUT:
     [JSON from financial-analyst]

     GEOPOLITICAL SECTION OUTPUT:
     [JSON from geopolitical-analyst]

     LABOR SECTION OUTPUT:
     [JSON from labor-analyst]

     ALL VALIDATED CLAIMS:
     [JSON array of all claims with validation status]

     PREVIOUS BRIEFING:
     [Previous full_briefing_md, or 'This is the inaugural briefing']

     PREDICTION TRACKING:
     - Pending: [N]
     - Due for review: [list]
     - Recent outcomes: [list]

     DOCUMENT COUNT: [total]
     NEW SINCE LAST: [delta]
     ACTIVE ALERT MATCHES: [list of alerts matched by new claims]

     Return structured JSON per your output format, including full_briefing_md.",
     run_in_background: false
   )
   ```

2. Parse the synthesizer's JSON response

### Phase 5: Store and Display

1. **Determine new version number**: Previous version + 1 (or 1 if inaugural)

2. **Store new briefing** in `rok_intel_briefings`:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_briefings" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
     -H "Content-Type: application/json" \
     -H "Prefer: return=representation" \
     -d '{
       "version": [new_version],
       "document_count": [total_docs],
       "claim_count": [total_claims],
       "prediction_count": [total_predictions],
       "executive_summary": "[executive_summary]",
       "key_developments": "[key_developments text]",
       "financial_section": "[financial_section_md]",
       "geopolitical_section": "[geopolitical_section_md]",
       "labor_section": "[labor_section_md]",
       "technology_section": null,
       "consensus_themes": [consensus_json],
       "contested_topics": [contested_json],
       "confidence_summary": [confidence_json],
       "full_briefing_md": "[complete markdown briefing]",
       "trigger_document_id": "[most recent doc id or null]"
     }'
   ```

3. **Display the full briefing** to the user (render the `full_briefing_md` content)

4. **Offer export**:
   ```
   Export this briefing to HTML/PDF/MD? (yes/no)
   ```
   If yes, trigger `/intel-briefing:intel-export briefing`

## Important Rules

- For `refresh`, always regenerate even if a recent briefing exists
- For `category:` filter, only generate that section (skip the other analyst agents). The synthesizer still runs but with only one section populated.
- Incremental synthesis: for non-refresh runs, only process claims newer than the last briefing but include previous sections for context
- If fewer than 3 total documents in the system, display a note: "Limited data -- briefing quality will improve with more sources. Currently based on [N] documents."
- If no claims exist at all, do not generate a briefing. Instead display: "No intelligence data found. Ingest documents first: /intel-briefing:intel-ingest"
- Each analyst agent has a WebSearch budget (max 5 queries each). Do not override this.
- The briefing-synthesizer uses the opus model for highest quality synthesis
- Always preserve previous briefing version -- never overwrite, only append new versions
- If an analyst agent fails or times out, proceed with the other section and note the gap in the briefing
