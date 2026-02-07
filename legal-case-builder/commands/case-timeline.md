# /case-timeline - Generate Case Timeline

Generate a chronological timeline of events from the case database. Events are extracted from documents and linked to source materials for attorney review.

## Usage

```
/case-timeline                                   # Full timeline
/case-timeline from:2024-01-01 to:2025-12-31    # Date range
/case-timeline focus:hvac_defect,hvac_failure     # Filter by tags
/case-timeline format:table                       # Table format
/case-timeline format:legal_brief                 # Attorney-ready format
/case-timeline significance:critical              # Only critical events
```

### Parameters
- **from** - Start date (ISO format)
- **to** - End date (ISO format)
- **focus** - Comma-separated tag topics to filter by
- **format** - `narrative` (default) | `table` | `legal_brief`
- **significance** - `all` (default) | `critical` | `supporting`
- **types** - Comma-separated event types: `communication`, `repair`, `failure`, `refusal`, `payment`, `legal_action`, `inspection`

## Execution Steps

### Step 1: Retrieve Timeline

Call the `get_timeline` MCP tool:

```
Tool: mcp__legal-case-builder__get_timeline
Parameters:
  date_from: [from parameter]
  date_to: [to parameter]
  event_types: [types parameter as list]
  tags: [focus parameter as list]
  significance: [significance parameter, default "all"]
```

### Step 2: Generate Report

If `format` is specified (or for any timeline with 10+ events), also call `generate_timeline_report`:

```
Tool: mcp__legal-case-builder__generate_timeline_report
Parameters:
  date_from: [from parameter]
  date_to: [to parameter]
  focus_topics: [focus parameter as list]
  format: [format parameter, default "narrative"]
```

### Step 3: Present Results

Display the formatted timeline:

```
═══════════════════════════════════════════════════════
CASE TIMELINE
═══════════════════════════════════════════════════════

[Generated timeline report content]

---

Total events: [count]
Critical: [count] | Supporting: [count] | Context: [count]
Date range: [earliest] to [latest]

NEXT STEPS:
  /case-timeline format:legal_brief   # Attorney-ready version
  /case-claims action:build            # Build claims from timeline
  /case-export type:timeline           # Export to HTML/PDF
═══════════════════════════════════════════════════════
```

### Step 4: Offer to Add Events

If the user has identified events missing from the timeline, offer to add them:

```
To add a timeline event, provide:
- Which document it relates to (Doc #ID)
- The date of the event
- Event type (communication/repair/failure/refusal/payment/legal_action/inspection)
- Brief description
- Significance (critical/supporting/context)
```

## Important Rules

- Every timeline event MUST cite a source document by ID
- Events should be presented in strict chronological order
- For legal_brief format, group by significance level (critical first)
- Critical events should be visually distinct (bold, marked)
- Include legal relevance notes when available
- If timeline is empty, suggest running /case-ingest first
