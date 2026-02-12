# /intel-validate - Validate Claims Against External Sources

Run external validation research on unvalidated claims using the research-validator agent. Searches for corroborating evidence, contradicting perspectives, and additional context to update claim confidence.

## Usage

```
/intel-briefing:intel-validate                      # Validate up to 10 unvalidated claims
/intel-briefing:intel-validate all                  # Validate all unvalidated claims (in batches)
/intel-briefing:intel-validate category:financial    # Only financial claims
/intel-briefing:intel-validate category:geopolitical # Only geopolitical claims
/intel-briefing:intel-validate limit:5              # Limit to 5 claims
/intel-briefing:intel-validate document:[doc_id]    # Validate claims from a specific document
```

### Parameters
- **all** - Validate all unvalidated claims (processes in batches of 10)
- **category** - Filter by claim category: `financial`, `geopolitical`, `technology`, `economic`, `market`, `policy`, `military`, `social`, `energy`, `labor`, `other`
- **limit** - Maximum number of claims to validate (default 10, max 50)
- **document** - UUID of a specific document to validate claims from

Initial request: $ARGUMENTS

## Execution Steps

### Phase 1: Query Unvalidated Claims

1. Build the query based on parameters:
   ```bash
   # Base query: unvalidated claims, ordered by confidence (highest first)
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?validation_status=eq.unvalidated&order=confidence_score.desc&limit=${LIMIT}&select=id,document_id,claim_text,category,subcategory,claim_type,confidence_score,tags,metadata" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

   Apply filters:
   - If `category:` specified, add `&category=eq.${CATEGORY}`
   - If `document:` specified, add `&document_id=eq.${DOC_ID}`
   - If `limit:` specified, use that limit (default 10)
   - If `all` specified, query all unvalidated (no limit, but process in batches)

2. If no unvalidated claims found:
   ```
   No unvalidated claims found matching your criteria.

   Claim Validation Status:
     Confirmed: [n]
     Partially Confirmed: [n]
     Unconfirmed: [n]
     Contradicted: [n]
     Contested: [n]
   ```
   Stop here.

3. Also fetch related document titles for context:
   ```bash
   # Get document titles for the claims
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?id=in.(${DOC_IDS})&select=id,title,author,trust_tier" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

4. Display claim list for user approval:
   ```
   UNVALIDATED CLAIMS: [N] found
   =========================================

   [1] "[claim_text]"
       Category: [category] | Type: [claim_type] | Confidence: [score]
       Source: [document_title] ([author])

   [2] "[claim_text]"
       ...

   [N] "[claim_text]"
       ...

   Proceed with validation of these [N] claims? (yes/no/select)
   ```
   - If user says "select", allow them to pick specific claims by number
   - If user says "no", stop

### Phase 2: Dispatch Validation

Process claims in batches of up to 10:

1. For each batch, dispatch the `research-validator` agent via the Task tool:
   ```
   Task(
     description: "Validate batch of [N] claims against external sources",
     prompt: "You are the research-validator agent. [Include agent instructions from agents/research-validator.md]

     CLAIMS TO VALIDATE:
     [JSON array of claims in this batch, each with:
       - claim_text
       - category
       - subcategory
       - claim_type
       - confidence_score
       - tags
     ]

     DOCUMENT CONTEXT:
     [For each unique document in the batch:
       - Title
       - Author
       - Trust Tier
     ]

     Validate the highest-impact claims first. Maximum 20 WebSearch queries total.
     Return structured JSON per your output format.",
     run_in_background: false
   )
   ```

2. Display progress during validation:
   ```
   Validating batch [X] of [Y]...
   Claims in batch: [N]
   [Waiting for research-validator agent...]
   ```

3. Parse the agent's JSON response for each claim's validation status

### Phase 3: Update Claims in Supabase

For each validated claim, update its record:

```bash
curl -s -X PATCH "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?id=eq.${CLAIM_ID}" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "validation_status": "[confirmed|partially_confirmed|unconfirmed|contradicted]",
    "validation_sources": [
      {
        "url": "[source_url]",
        "title": "[source_title]",
        "summary": "[what it says about the claim]",
        "date": "[source_date]"
      }
    ]
  }'
```

### Phase 4: Display Results

Show validation results summary:

```
=========================================
VALIDATION COMPLETE
=========================================
Claims Validated: [N]

Results:
  Confirmed:            [n] - Multiple sources corroborate
  Partially Confirmed:  [n] - Some support with caveats
  Unconfirmed:          [n] - No sources address directly
  Contradicted:         [n] - Sources actively disagree

Detailed Results:
-----------------------------------------
[1] "[claim_text]"
    Status: [STATUS]
    Sources:
      - [source_title] ([url]) - [summary]
      - [source_title] ([url]) - [summary]
    Counter-arguments: [if any]
    Notes: [validator notes]

[2] "[claim_text]"
    ...

-----------------------------------------
Additional Context Discovered:
  - [topic]: [url] - [relevance]
  - [topic]: [url] - [relevance]

Temporal Notes:
  - [any time-sensitive observations]

Research Summary: [validator's overall summary]
=========================================

REMAINING UNVALIDATED: [N]

NEXT STEPS:
  /intel-briefing:intel-validate                    # Validate next batch
  /intel-briefing:intel-briefing refresh            # Refresh briefing with validated data
  /intel-briefing:intel-library stats               # View library statistics
```

If processing `all` and more batches remain:
```
Batch [X] of [Y] complete. Processing next batch...
```
Continue until all batches are processed, then show cumulative summary.

## Important Rules

- **Maximum 10 claims per validation batch** to control API usage and stay within the research-validator's WebSearch budget (max 20 searches per invocation)
- **Prioritize high-confidence claims first** -- they have the most impact on briefing quality. The query orders by confidence_score DESC.
- Show validation sources (URLs) in results -- transparency is critical for trust
- Never fabricate validation results -- if the agent cannot validate a claim, mark it "unconfirmed" not "confirmed"
- For `all` mode, pause between batches to show intermediate results and allow the user to stop
- If the research-validator agent fails on a batch, log the error, mark those claims as still "unvalidated", and continue with the next batch
- After validation completes, suggest refreshing the master briefing if 5+ claims were newly validated
- Track the total number of WebSearch queries used across batches to maintain awareness of API consumption
