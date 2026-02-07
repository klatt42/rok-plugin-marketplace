# /case-search - Search Case Documents

Search the Legal Case Builder database for documents matching a query with optional filters. Supports full-text search, email topic filtering, and thread reconstruction.

## Usage

```
/case-search query:"HVAC compressor failure"
/case-search query:"rent credit" type:email sender:"Irina"
/case-search query:"ProPress" tags:hvac_defect,construction_defect
/case-search query:"OPEX" from:2024-01-01 to:2024-12-31
/case-search topic:hvac_emergency
/case-search thread:"HVAC - Compressor"
/case-search doc:42                              # Get specific document by ID
```

### Parameters
- **query** - Full-text search terms
- **type** - Filter by document type: `email`, `invoice`, `lease`, `letter`, etc.
- **tags** - Comma-separated tag filters (all must match)
- **from** - Start date (ISO format: YYYY-MM-DD)
- **to** - End date (ISO format: YYYY-MM-DD)
- **sender** - Filter emails by sender name or email
- **topic** - Search emails by topic tag or keyword
- **thread** - Find all emails in a thread by subject
- **doc** - Get full details for a specific document ID
- **text** - Include full raw text in results (default: false)

## Execution Steps

### Determine Search Type

Based on the parameters provided, choose the appropriate MCP tool:

**If `doc:` provided** — Single document lookup:
```
Tool: mcp__legal-case-builder__get_document
Parameters:
  document_id: [doc parameter]
  include_text: [text parameter, default false]
```

**If `thread:` provided** — Thread reconstruction:
```
Tool: mcp__legal-case-builder__get_thread
Parameters:
  subject_contains: [thread parameter]
```

**If `topic:` provided** — Email topic search:
```
Tool: mcp__legal-case-builder__search_emails_by_topic
Parameters:
  topic: [topic parameter]
  participant: [sender parameter if provided]
  date_from: [from parameter]
  date_to: [to parameter]
```

**Otherwise** — Full-text document search:
```
Tool: mcp__legal-case-builder__search_documents
Parameters:
  query: [query parameter]
  doc_type: [type parameter]
  tags: [tags parameter as list]
  date_from: [from parameter]
  date_to: [to parameter]
  sender: [sender parameter]
  max_results: 20
```

### Present Results

For document search results:
```
═══════════════════════════════════════════════════════
SEARCH RESULTS: "[query]"
═══════════════════════════════════════════════════════

Found: [count] documents

1. [Doc #ID] [TYPE] - [filename]
   Summary: [summary snippet]
   Tags: [tag1, tag2, ...]
   [For emails: Date: [date] | From: [sender] | Subject: [subject]]

2. [Doc #ID] ...

═══════════════════════════════════════════════════════
```

For thread results:
```
═══════════════════════════════════════════════════════
EMAIL THREAD: "[subject]"
═══════════════════════════════════════════════════════

Messages: [count] | Date range: [first] to [last]

1. [date] - [sender] → [recipients]
   Subject: [subject]
   Summary: [summary]

2. [date] ...

═══════════════════════════════════════════════════════
```

## Important Rules

- Always show document IDs — users need them for /case-claims evidence linking
- For email results, always show date, sender, and subject
- Keep result display concise — use summaries, not full text
- If no results found, suggest alternative search terms or filters
- Full-text search supports FTS5 syntax (AND, OR, NOT, "phrase match", prefix*)
