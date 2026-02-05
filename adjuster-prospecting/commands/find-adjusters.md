# Find Adjusters

You are executing an insurance adjuster discovery workflow for Prism Specialties DMV. Your goal is to find carrier adjusters who handle restoration losses in the DMV area (DC, Maryland, Virginia).

## Input

The user will provide one or more of:
- **Carrier name** (e.g., "State Farm", "Travelers", "Crawford")
- **Geographic focus** (e.g., "Fairfax County", "Montgomery County", "DC") — default is full DMV
- **Loss type filter** (e.g., "fire", "water", "contents", "large loss", "commercial")

If the user provides none of these, ask which carrier(s) they want to search first.

## Process

### Step 1: Construct Search Queries

Build targeted search queries based on the input:

**LinkedIn-style queries** (use WebSearch):
- `"[carrier name]" "claims adjuster" OR "property adjuster" OR "field adjuster" "[location]" site:linkedin.com`
- `"[carrier name]" "large loss" OR "commercial claims" "[state]" site:linkedin.com`
- `"[carrier name]" "claims manager" OR "team lead" "property" "[location]" site:linkedin.com`

**Carrier office searches**:
- `"[carrier name]" claims office "[city]" "[state]"`
- `"[carrier name]" property claims "[location]" phone`

**State DOI license lookups** (if specific name found):
- Maryland: https://sbs.naic.org/solar-external-lookup/
- Virginia: https://scc.virginia.gov/pages/Bureau-of-Insurance
- DC: https://disb.dc.gov/service/verify-insurance-license

### Step 2: Execute Searches

Run at least 3-5 web searches with different query variations. Cast a wide net:
1. Primary carrier + adjuster title + location
2. Carrier + "claims office" + specific city/county
3. Carrier + specialty (large loss, commercial, contents) + DMV
4. Independent adjusting firms if carrier uses them
5. LinkedIn group or industry association results

### Step 3: Compile Results

For each adjuster found, extract:
- **Name**
- **Title** (field adjuster, senior adjuster, team lead, etc.)
- **Carrier or firm**
- **Location/territory** (as specific as possible)
- **Loss types handled** (property, commercial, contents, large loss)
- **LinkedIn URL** (if found)
- **Contact info** (email, phone, office address — if publicly available)
- **Source** (where you found this information)

### Step 4: Present Results

Output a structured table:

```
## Adjuster Search Results: [Carrier] — [Location]

| Name | Title | Territory | Loss Types | LinkedIn | Source |
|------|-------|-----------|------------|----------|--------|
| ... | ... | ... | ... | ... | ... |

Found: [X] adjusters
```

After the table, provide:
- **Quick analysis**: Which adjusters look most promising for Prism (based on title seniority, territory overlap, loss type match)
- **Suggested next steps**: "Run `/adjuster-prospecting:adjuster-profile [name]` on the top prospects"
- **Search gaps**: What you couldn't find and alternative approaches to try

### Step 5: Export to Excel and PDF

After presenting results in the chat, export them to professional files:

1. Construct a JSON object from the compiled results:
   - `type`: `"adjusters"`
   - `carrier`: The carrier name searched (e.g., "State Farm")
   - `region`: The geographic area searched (default "DMV")
   - `date`: Today's date in YYYY-MM-DD format
   - `report_type`: `"Search"` (use `"Profiles"` for profile reports, `"Pipeline"` for pipeline exports)
   - `search_summary`: Brief description of the search performed
   - `records`: Array of adjuster objects, each with:
     - `name`, `title`, `carrier`, `territory`
     - `loss_types` (array of strings)
     - `linkedin_url`, `contact_info`, `source`, `notes`
     - `priority`: "high", "medium", or "low" — based on territory overlap with Prism DMV, loss type relevance, and title seniority
     - `category`: one of "adjuster", "manager", "agent_warm_intro", "ia_firm", "other"
   - `analysis`: The quick analysis text from Step 4
   - `next_steps`: Array of suggested next step strings from Step 4

2. **Exclude `ia_firm` records** from the carrier report — Independent Adjusting Firms are tracked separately.

3. Write the JSON to a temp file and run the export:
   ```bash
   cat > /tmp/prospecting_export.json << 'EXPORT_EOF'
   { ... the JSON payload ... }
   EXPORT_EOF

   ~/.claude/scripts/.venv/bin/python3 ~/.claude/scripts/prospecting_export.py \
     --input /tmp/prospecting_export.json

   rm /tmp/prospecting_export.json
   ```

4. Report the output file paths to the user:
   ```
   Exported to:
   - Excel: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/{Carrier}/{filename}.xlsx
   - PDF: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/{Carrier}/{filename}.pdf
   ```

## Rules

- Only use publicly available information
- Do not fabricate adjuster names or profiles — only report what you actually find in search results
- If a search returns no results, say so and suggest alternative search terms
- Prioritize field adjusters and team leads over desk adjusters (field adjusters are on-site decision makers)
- Flag any adjusters who appear to handle contents or specialty losses specifically — these are highest priority for Prism
- If you find an independent adjusting firm office in the DMV, note which carriers they serve
