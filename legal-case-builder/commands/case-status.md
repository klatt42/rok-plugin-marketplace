# /case-status - Database Statistics and Coverage

Display comprehensive statistics about the Legal Case Builder database including document counts, tag distribution, timeline coverage, claim status, and processing progress.

## Usage

```
/case-status
```

No parameters needed.

## Execution Steps

### Step 1: Get Statistics

Call the `get_stats` MCP tool:

```
Tool: mcp__legal-case-builder__get_stats
```

### Step 2: Present Dashboard

```
═══════════════════════════════════════════════════════
LEGAL CASE BUILDER - DATABASE STATUS
═══════════════════════════════════════════════════════

## Documents
| Type | Count | Processed |
|------|-------|-----------|
[table from documents_by_type]

**Total:** [total_documents] | **Processed:** [total_processed] | **Pending:** [unprocessed_documents]

## Date Coverage
Earliest email: [date_range.earliest]
Latest email: [date_range.latest]
Email threads: [total_email_threads]

## Tags
Total tags applied: [total_tags]

Top tags:
[tag_distribution - top 15]

## Timeline
Total events: [total_timeline_events]
[event type breakdown]

## Legal Claims
Total claims: [total_claims]
[claim type breakdown]

Evidence links: [from claim counts]

## Parties
Total known parties: [total_parties]

## Lease Provisions
Total indexed: [total_lease_provisions]

═══════════════════════════════════════════════════════

QUICK ACTIONS:
  /case-ingest                  # Ingest more documents
  /case-search query:"..."      # Search the database
  /case-timeline                # View chronological timeline
  /case-claims                  # Review legal claims
  /case-export type:full        # Export complete case report
═══════════════════════════════════════════════════════
```

## Important Rules

- Always present the full dashboard — it's a quick overview
- Highlight any issues (unprocessed documents, empty sections)
- If the database is empty, suggest running /case-ingest first
