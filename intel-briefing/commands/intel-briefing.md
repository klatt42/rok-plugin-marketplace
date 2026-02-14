# /intel-briefing - Generate Master Intelligence Briefing

Generate or view the cumulative intelligence master briefing, synthesizing all ingested documents into four analytical pillars: financial outlook, geopolitical analysis, AI & technology, and labor markets, plus prediction tracking and cross-domain themes.

## Usage

```
/intel-briefing:intel-briefing                    # Show current briefing
/intel-briefing:intel-briefing refresh            # Force regeneration from all data
/intel-briefing:intel-briefing category:financial  # Focus on financial section only
/intel-briefing:intel-briefing category:geopolitical # Focus on geopolitical section only
/intel-briefing:intel-briefing category:technology   # Focus on AI & technology section only
/intel-briefing:intel-briefing category:labor        # Focus on labor section only
/intel-briefing:intel-briefing since:2026-01-01    # Only include data since date
```

### Parameters
- **refresh** - Force regeneration even if a recent briefing exists
- **category** - Focus on a single section: `financial`, `geopolitical`, `technology`, `labor`
- **since** - Only consider data after this date (ISO format YYYY-MM-DD)

### Output Folder
All exported files (MD, HTML) are written to:
```
/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Outputs/briefings/
```
This folder is the single source of truth for briefing outputs. Never export to Desktop root or /tmp.

Initial request: $ARGUMENTS

## Execution Steps

### Phase 1: Check Current State

1. **Determine version number from BOTH sources** (use whichever is higher):

   a. Query the latest briefing from Supabase:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_briefings?order=version.desc&limit=1&select=id,version,created_at,document_count,claim_count,prediction_count,executive_summary,full_briefing_md" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

   b. Scan the output folder for existing briefing files:
   ```bash
   ls /mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Outputs/briefings/*intel-briefing_v*.md 2>/dev/null | sort -V | tail -1
   ```
   Extract the version number from the filename pattern `*_v[N].*`. The highest version from either Supabase or the output folder is the **current version**. The new briefing will be current + 1.

   **IMPORTANT**: If the output folder shows a higher version than Supabase, prior briefings were generated in sessions where Supabase storage was unavailable or the DB was reset. Always respect the output folder version as authoritative.

2. Parse the response:
   - If no briefing exists in EITHER source, proceed to Phase 2 to generate the inaugural briefing
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

5. Get previous briefing sections (financial_section, geopolitical_section, technology_section, labor_section) for delta detection context

6. **File-based fallback for previous briefing**: If Supabase has no previous briefing (or the version in Supabase is lower than the output folder), load the most recent `*_intel-briefing_v*.md` file from the output folder:
   ```bash
   LATEST_FILE=$(ls /mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Outputs/briefings/*intel-briefing_v*.md 2>/dev/null | sort -V | tail -1)
   ```
   Read this file's content and use it as the `PREVIOUS BRIEFING` context for all analyst agents and the synthesizer. This ensures cumulative context is preserved even when Supabase has been reset.

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

If `category:financial` is specified, only dispatch financial. If `category:geopolitical`, only geopolitical. If `category:technology`, only technology. If `category:labor`, only labor. Otherwise dispatch all four analysts in parallel.

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

4. **Dispatch technology-analyst** agent (background):
   ```
   Task(
     description: "Technology synthesis for master briefing",
     prompt: "You are the technology-analyst agent. [Include agent instructions from agents/technology-analyst.md]

     TECHNOLOGY CLAIMS:
     [JSON array of all technology/ai/semiconductor/autonomous category claims]

     PREVIOUS TECHNOLOGY SECTION:
     [Previous briefing's technology section text, or 'This is the inaugural technology section']

     CURRENT DATE: [today's date]

     Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

5. **Dispatch labor-analyst** agent (background):
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

6. Collect results from all agents via TaskOutput (block: true):
   ```
   TaskOutput(task_id: "<financial_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<geopolitical_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<technology_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<labor_task_id>", block: true, timeout: 120000)
   ```

Display:
```
SPECIALIZED ANALYSIS COMPLETE
Financial Section: [Ready / Skipped / Error]
Geopolitical Section: [Ready / Skipped / Error]
Technology Section: [Ready / Skipped / Error]
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

     TECHNOLOGY SECTION OUTPUT:
     [JSON from technology-analyst]

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

     BRIEFING VERSION: v[N] (determined in Phase 1 from highest of Supabase or output folder + 1)
     DOCUMENT COUNT: [total across ALL sessions, not just current]
     NEW SINCE LAST: [delta - documents added since previous briefing]
     ACTIVE ALERT MATCHES: [list of alerts matched by new claims]

     IMPORTANT: The full_briefing_md header MUST use the correct version number, total document count, and new-since-last count. Do NOT label as 'inaugural' if previous briefing versions exist. Check the version number provided above.",
     run_in_background: false
   )
   ```

2. Parse the synthesizer's JSON response

### Phase 5: Store and Display

1. **Determine new version number**: Use the highest version found in Phase 1 (from Supabase OR output folder) + 1. If neither has any briefings, use version 1.

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
       "technology_section": "[technology_section_md]",
       "consensus_themes": [consensus_json],
       "contested_topics": [contested_json],
       "confidence_summary": [confidence_json],
       "full_briefing_md": "[complete markdown briefing]",
       "trigger_document_id": "[most recent doc id or null]"
     }'
   ```

3. **Display the full briefing** to the user (render the `full_briefing_md` content)

4. **Auto-export to output folder** (always, no prompt needed):
   ```
   Output folder: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Outputs/briefings/
   ```
   - Write the `full_briefing_md` to `Intel_Briefing_v[N]_[YYYY-MM-DD].md`
   - Generate a self-contained HTML version and write to `Intel_Briefing_v[N]_[YYYY-MM-DD].html`
   - Use a dark-themed HTML template with print-friendly CSS for PDF-via-browser
   - Display: "Exported to PlugIn-Intel-Outputs/briefings/ (MD + HTML)"

## Important Rules

- For `refresh`, always regenerate even if a recent briefing exists
- For `category:` filter, only generate that section (skip the other analyst agents). The synthesizer still runs but with only one section populated.
- **Cumulative context is critical**: Always load the previous briefing (from Supabase or output folder file) and pass it to ALL analyst agents and the synthesizer. Each briefing must build on prior analysis, not start fresh.
- Incremental synthesis: for non-refresh runs, only process claims newer than the last briefing but include previous sections for context
- If fewer than 3 total documents in the system, display a note: "Limited data -- briefing quality will improve with more sources. Currently based on [N] documents."
- If no claims exist at all, do not generate a briefing. Instead display: "No intelligence data found. Ingest documents first: /intel-briefing:intel-ingest"
- Each analyst agent has a WebSearch budget (max 5 queries each). Do not override this.
- The briefing-synthesizer uses the opus model for highest quality synthesis
- Always preserve previous briefing version -- never overwrite, only append new versions
- If an analyst agent fails or times out, proceed with the other section and note the gap in the briefing
