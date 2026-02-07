# /case-ingest - Ingest Documents into Case Database

Scans a folder for PDF files and ingests them into the Legal Case Builder SQLite database. Extracts text, detects document types, parses email metadata, generates AI summaries, and auto-categorizes with topic tags.

## Usage

```
/case-ingest                                    # Ingest from default Elion case folder
/case-ingest folder:/path/to/pdfs               # Ingest from specific folder
/case-ingest folder:/path/to/pdfs type:email     # Force all files as email type
/case-ingest force:true                          # Re-process already ingested files
```

### Parameters
- **folder** - Path to folder containing PDFs (default: Elion-HVAC Legal Battle folder)
- **type** - Override auto-detection: `email`, `invoice`, `lease`, `letter`, `analysis`, `proposal`, `contract`, `work_order`, `estoppel`, `other`
- **force** - `true` to re-ingest files even if already in database

## Execution Steps

### Step 1: Ingest PDFs

Call the `ingest_folder` MCP tool from the `legal-case-builder` MCP server:

```
Tool: mcp__legal-case-builder__ingest_folder
Parameters:
  folder_path: [folder parameter or default]
  doc_type: [type parameter if provided]
  force_reprocess: [force parameter, default false]
```

This will:
- Scan the folder recursively for .pdf files
- Extract text from each PDF using pdfplumber
- Compute SHA-256 hash for deduplication
- Auto-detect document type (email, invoice, lease, etc.)
- For emails: parse sender, recipients, date, subject, thread ID
- Store everything in the SQLite database

Present the results:
```
═══════════════════════════════════════════════════════
DOCUMENT INGESTION COMPLETE
═══════════════════════════════════════════════════════

PDFs found: [total]
Ingested: [count]
Skipped (already in DB): [count]
Errors: [count]

[If errors, list them]
═══════════════════════════════════════════════════════
```

### Step 2: Generate Summaries

Call the `process_summaries` MCP tool to AI-summarize all newly ingested documents:

```
Tool: mcp__legal-case-builder__process_summaries
Parameters:
  batch_size: 20
```

Repeat this call until all documents are processed (check `remaining_unprocessed` in response). Report progress:

```
Summarizing documents... [summarized] of [total] complete
```

### Step 3: Auto-Categorize

Call the `auto_categorize` MCP tool to assign topic tags:

```
Tool: mcp__legal-case-builder__auto_categorize
```

Report categorization results.

### Step 4: Present Summary

Call `get_stats` to show the final database state:

```
Tool: mcp__legal-case-builder__get_stats
```

Present:
```
═══════════════════════════════════════════════════════
DATABASE STATUS
═══════════════════════════════════════════════════════

Documents by type:
  Emails: [count]
  Invoices: [count]
  [etc.]

Total documents: [count]
Processed: [count]
Email threads: [count]
Tags applied: [count]
Date range: [earliest] to [latest]

NEXT STEPS:
  /case-search query:"HVAC"        # Search the database
  /case-timeline                    # Generate chronological timeline
  /case-claims action:build         # Start building legal claims
  /case-status                      # View full statistics
═══════════════════════════════════════════════════════
```

## Important Rules

- ALWAYS show progress during long ingestion runs
- If the folder has more than 100 PDFs, suggest running summaries in batches
- The process_summaries step uses Haiku for cost efficiency
- auto_categorize also uses Haiku
- Do NOT skip the summarization step — summaries are needed for search and categorization
- If errors occur during ingestion, still proceed with successfully ingested files
