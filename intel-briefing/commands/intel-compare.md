# Source Comparison

Compare prediction accuracy and analytical views between different sources.

## Usage

```
/intel-briefing:intel-compare                              # List all sources
/intel-briefing:intel-compare sources:"Andrei Jikh,Ray Dalio"
/intel-briefing:intel-compare sources:"Andrei Jikh,Ray Dalio" category:financial
```

Initial request: $ARGUMENTS

## Workflow

### No args -- List All Sources

1. Query `rok_intel_sources` ordered by `documents_analyzed DESC`:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_sources?order=documents_analyzed.desc" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

2. Display formatted table:

```
INTEL SOURCES
=============

| # | Source | Type | Trust | Expertise | Docs | Accuracy |
|---|--------|------|-------|-----------|------|----------|
| 1 | Andrei Jikh | youtube_channel | MEDIUM | crypto, equities, macro | 5 | 50.00% |
| 2 | Ray Dalio | analyst | HIGH | macro, debt-cycles, monetary-policy | 3 | N/A |
| 3 | Peter Zeihan | analyst | MEDIUM | geopolitics, demographics, energy | 4 | 62.50% |
| 4 | The Economist | publication | HIGH | macro, policy, geopolitics | 2 | N/A |

Total sources: 4

Compare sources:
  /intel-briefing:intel-compare sources:"Andrei Jikh,Ray Dalio"
```

3. If no sources exist, display:

```
No sources registered yet.

Sources are created automatically during document ingestion.
```

### With "sources" -- Compare Sources

1. Parse source names from the comma-separated list (trim whitespace).
2. Validate that at least 2 sources are provided. If only 1, prompt the user for a second.

3. For each source, fetch the source profile:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_sources?source_name=eq.[source_name]" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

4. If a source name is not found, try a case-insensitive partial match:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_sources?source_name=ilike.*[partial]*" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

5. For each source, fetch document count:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?author=eq.[source_name]&select=id" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
  -H "Prefer: count=exact"
```

6. For each source, fetch claims via their documents:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?document_id=in.([doc_ids])&select=id,category,claim_type,subcategory,confidence_score,claim_text,tags" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

7. For each source, fetch predictions via their documents:

```bash
curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?document_id=in.([doc_ids])&select=id,category,prediction_text,outcome,initial_confidence" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

8. If `category` filter is provided, filter claims and predictions to only those matching the specified category.

9. Compute per-source metrics:
   - **Total Claims**: count of claims
   - **Claims by Category**: group claims by `category`, count each
   - **Predictions Made**: count of predictions
   - **Predictions Evaluated**: count where `outcome` is not 'pending'
   - **Accuracy**: (correct + 0.5 * partially_correct) / total_evaluated * 100
   - **Brier Score**: If predictions have initial_confidence and outcomes, compute mean squared error. For correct outcomes: (1 - confidence)^2. For incorrect: confidence^2. For partially_correct: (0.5 - confidence)^2.

10. Generate the comparison report:

```
SOURCE COMPARISON REPORT
========================

| Metric | [Source A] | [Source B] |
|--------|-----------|-----------|
| Trust Tier | [tier] | [tier] |
| Source Type | [type] | [type] |
| Documents Analyzed | [count] | [count] |
| Total Claims | [count] | [count] |
| Financial Claims | [count] | [count] |
| Geopolitical Claims | [count] | [count] |
| Technology Claims | [count] | [count] |
| Economic Claims | [count] | [count] |
| Other Claims | [count] | [count] |
| Predictions Made | [count] | [count] |
| Predictions Evaluated | [count] | [count] |
| Accuracy | [pct]% | [pct]% |
| Brier Score | [score] | [score] |
```

11. Perform agreement analysis by comparing claims with matching subcategories:

```
AGREEMENT ANALYSIS
==================
Topics where sources agree:
  - [subcategory]: [brief summary of shared conclusion]
  - [subcategory]: [brief summary of shared conclusion]

Topics where sources disagree:
  - [subcategory]: [Source A] says [conclusion A]; [Source B] says [conclusion B]
```

   Agreement detection: Two claims share the same subcategory AND reach the same directional conclusion (both bullish/bearish, both predict increase/decrease, both support/oppose).

   Disagreement detection: Two claims share the same subcategory BUT reach opposite directional conclusions.

   If no overlapping subcategories exist, display "No overlapping topics found for comparison."

12. Compare domain expertise:

```
DOMAIN EXPERTISE
================
  Shared:         [expertise1, expertise2]
  [Source A] only: [expertise3, expertise4]
  [Source B] only: [expertise5, expertise6]
```

   Compute by comparing the `domain_expertise` arrays from `rok_intel_sources`.

13. If comparing more than 2 sources, extend the table columns accordingly (up to 4 sources max for readability).

14. Offer next steps:

```
Next Steps:
  - Deep dive on a source: /intel-briefing:intel-compare sources:"[name]" category:financial
  - View predictions: /intel-briefing:intel-predict
  - Full briefing: /intel-briefing:intel-brief
```

### Category-Filtered Comparison

When `category` is specified:

1. Filter all claim and prediction queries to only include items matching the category
2. Adjust the comparison table to show subcategory breakdown instead of category breakdown:

```
FILTERED COMPARISON: financial
==============================

| Metric | [Source A] | [Source B] |
|--------|-----------|-----------|
| Trust Tier | [tier] | [tier] |
| Financial Claims | [count] | [count] |
| - fed-policy | [count] | [count] |
| - gold-silver | [count] | [count] |
| - crypto | [count] | [count] |
| - dollar-policy | [count] | [count] |
| Financial Predictions | [count] | [count] |
| Evaluated | [count] | [count] |
| Accuracy (financial) | [pct]% | [pct]% |
```

3. Agreement/disagreement analysis is also scoped to the filtered category only.

## Rules

- Need at least 2 sources to run a comparison -- prompt user if only 1 provided
- Maximum 4 sources per comparison for table readability
- If a source has no predictions evaluated, show "N/A" for accuracy and Brier score
- Agreement detection: same subcategory + same directional conclusion
- Disagreement detection: same subcategory + opposite directional conclusions
- Source name matching is case-insensitive; try partial match if exact match fails
- Category filter must be one of: financial, geopolitical, technology, economic, market, policy, military, social, energy, other
- Format all percentages to 2 decimal places
- Brier scores are displayed to 4 decimal places (lower is better; range 0.0000 to 1.0000)
- When a source has zero documents, display 0 for all counts rather than skipping the source
- Do NOT fabricate comparison data -- only report what exists in the database
