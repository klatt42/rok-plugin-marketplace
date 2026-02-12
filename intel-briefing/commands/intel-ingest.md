# /intel-ingest - Ingest Document into Intelligence System

Ingest a document into the intelligence briefing system. Extracts claims, predictions, and key points, validates them against external sources, stores in Supabase, and optionally triggers a master briefing update.

## Usage

```
/intel-briefing:intel-ingest <path-or-url>
/intel-briefing:intel-ingest                    # Process watch folder
/intel-briefing:intel-ingest --skip-validation   # Skip external validation
/intel-briefing:intel-ingest --skip-briefing     # Don't update master briefing
```

### Parameters
- **$ARGUMENTS** - A file path, URL, or empty (triggers watch folder scan)
- **--skip-validation** - Skip Phase 4 (external claim validation)
- **--skip-briefing** - Skip Phase 6 (master briefing update)

Initial request: $ARGUMENTS

## Execution Steps

### Phase 1: Source Detection

Determine the source type from $ARGUMENTS:

1. **If $ARGUMENTS is empty**, scan the watch folder:
   ```
   Watch folder: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/
   ```
   - List all files NOT in the `processed/` subfolder
   - Filter to supported extensions: `.md`, `.txt`, `.pdf`
   - Skip hidden files (starting with `.`) and system files
   - Display the file list with sizes and types to the user
   - Ask: "Process these [N] files? (yes/no/select specific)"
   - If user confirms, process each file sequentially through Phases 2-7, then show cumulative summary

2. **If $ARGUMENTS is a URL**:
   - YouTube URL (contains `youtube.com` or `youtu.be`):
     a. Check if `yt-dlp` is available: `which yt-dlp`
     b. If yes: extract transcript via `yt-dlp --write-auto-sub --sub-lang en --skip-download -o "/tmp/yt-intel-%(id)s" "$URL"` then read the subtitle file
     c. If no yt-dlp: use WebFetch to get the YouTube page content as fallback
     d. Also extract video title, channel name, publish date from the page
   - Web URL (any other URL):
     a. Use WebFetch to fetch the article content
     b. Extract title, author, publish date from the page

3. **If $ARGUMENTS is a file path**:
   - `.md` file: Read file (expects YAML frontmatter with `title:`, `tags:`, `createdAt:` fields, bullet-point body, Sources section)
   - `.txt` file: Read file (likely a transcript with inline timestamps)
   - `.pdf` file: Read file (PDF content extraction)
   - If file does not exist, inform user and stop

4. Set `source_type`: `youtube`, `url`, `pdf`, `markdown`, or `text`

Display:
```
SOURCE DETECTED
Type: [source_type]
Path/URL: [path or url]
```

### Phase 2: Content Extraction

1. Read the document content using the Read tool
2. Parse metadata based on source type:
   - **MD files**: Parse YAML frontmatter to extract `title`, `tags`, `createdAt`. Parse Sources section for attribution URLs.
   - **TXT transcripts**: Extract title from first line. Look for YouTube URL from timestamps or metadata lines.
   - **PDF files**: Extract title from first heading or filename. Note page count.
   - **URLs**: Use title and metadata extracted in Phase 1.
3. Generate SHA256 content hash for deduplication:
   ```bash
   echo -n "[first 5000 chars of content]" | sha256sum | awk '{print $1}'
   ```
4. Check Supabase `rok_intel_documents` for existing content_hash:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?content_hash=eq.${HASH}&select=id,title" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```
5. If duplicate found, inform user:
   ```
   DUPLICATE DETECTED: "[title]" already ingested (ID: [id])
   Skipping. Use --force to re-process.
   ```
   Skip to next file (if batch) or stop.

Display:
```
CONTENT EXTRACTED
Title: [title]
Author: [author or "Unknown"]
Date: [publish_date or "N/A"]
Word Count: ~[estimated word count]
Content Hash: [hash]
```

### Phase 3: Document Analysis

1. Look up the source author in `rok_intel_sources`:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_sources?source_name=ilike.%25${AUTHOR}%25&select=id,source_name,trust_tier,domain_expertise" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```
   If not found, default trust_tier to `STANDARD`.

2. Dispatch the `document-analyst` agent via the Task tool:
   ```
   Task(
     description: "Analyze document for claims, predictions, and key intelligence",
     prompt: "You are the document-analyst agent. [Include agent instructions from agents/document-analyst.md]

     DOCUMENT TEXT:
     [full document text]

     METADATA:
     - source_type: [type]
     - author: [author]
     - date: [date]
     - url: [url if available]
     - trust_tier: [tier]

     Return structured JSON per your output format.",
     run_in_background: false
   )
   ```

3. Parse the agent's JSON response. Extract: summary, classification, topics, key_points, claims, predictions, notable_quotes.

Display:
```
DOCUMENT ANALYSIS COMPLETE
Classification: [classification]
Topics: [topic1, topic2, ...]
Key Points: [N] extracted
Claims: [N] extracted (Financial: [n] | Geopolitical: [n] | Technology: [n] | Other: [n])
Predictions: [N] extracted
Notable Quotes: [N] extracted
```

### Phase 4: Claim Validation (unless --skip-validation)

If `--skip-validation` is present in $ARGUMENTS, skip to Phase 5.

1. Dispatch the `research-validator` agent via the Task tool:
   ```
   Task(
     description: "Validate extracted claims against external sources",
     prompt: "You are the research-validator agent. [Include agent instructions from agents/research-validator.md]

     CLAIMS TO VALIDATE:
     [JSON array of extracted claims with search_suggestion fields]

     DOCUMENT CONTEXT:
     - Title: [title]
     - Author: [author]
     - Trust Tier: [tier]
     - Classification: [classification]

     Validate the highest-impact claims. Return structured JSON per your output format.",
     run_in_background: false
   )
   ```

2. Parse the validation results. Update each claim's validation_status from the response.

Display:
```
VALIDATION COMPLETE
Claims Validated: [N] of [total]
  Confirmed: [n]
  Partially Confirmed: [n]
  Unconfirmed: [n]
  Contradicted: [n]
```

### Phase 5: Supabase Storage

Store all extracted data using curl to the Supabase REST API.

1. **Insert document** into `rok_intel_documents`:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
     -H "Content-Type: application/json" \
     -H "Prefer: return=representation" \
     -d '{
       "source_type": "[type]",
       "source_path": "[path]",
       "source_url": "[url]",
       "title": "[title]",
       "author": "[author]",
       "publish_date": "[date]",
       "content_hash": "[hash]",
       "raw_summary": "[summary from analysis]",
       "word_count": [count],
       "trust_tier": "[tier]",
       "classification": "[classification]",
       "topics": ["topic1", "topic2"],
       "tags": ["tag1", "tag2"],
       "processed": true,
       "metadata": {}
     }'
   ```
   Capture the returned document `id`.

2. **Insert claims** into `rok_intel_claims` (batch insert):
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
     -H "Content-Type: application/json" \
     -H "Prefer: return=representation" \
     -d '[
       {
         "document_id": "[doc_id]",
         "claim_text": "[claim]",
         "category": "[category]",
         "subcategory": "[subcategory]",
         "claim_type": "[type]",
         "confidence_score": [score],
         "validation_status": "[status]",
         "validation_sources": [sources_json],
         "tags": ["tag1"],
         "expires_at": "[date or null]"
       }
     ]'
   ```

3. **Insert predictions** into `rok_intel_predictions` (batch insert):
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}" \
     -H "Content-Type: application/json" \
     -H "Prefer: return=representation" \
     -d '[
       {
         "document_id": "[doc_id]",
         "prediction_text": "[prediction]",
         "category": "[category]",
         "subcategory": "[subcategory]",
         "timeframe": "[timeframe]",
         "target_date": "[date or null]",
         "initial_confidence": [score],
         "current_confidence": [score],
         "source_author": "[author]",
         "tags": ["tag1"]
       }
     ]'
   ```

4. **Update/insert source** into `rok_intel_sources`:
   - First check if source exists by name
   - If exists: PATCH to increment `documents_analyzed` and update `last_analyzed`
   - If not: POST new source record with `trust_tier: "STANDARD"` and `documents_analyzed: 1`

5. **Check active alerts** for matches against new claims:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_alerts?active=eq.true&select=id,topic,keywords" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```
   For each alert, check if any claim text or topic matches the alert keywords. If matches found, display alert notifications and update the alert's `match_count` and `last_matched`.

Display:
```
STORAGE COMPLETE
Document ID: [uuid]
Claims Stored: [N]
Predictions Stored: [N]
Source Updated: [author] (Trust: [tier], Documents: [count])
Alert Matches: [N] (if any, list alert topics)
```

### Phase 6: Master Briefing Update (unless --skip-briefing)

If `--skip-briefing` is present in $ARGUMENTS, skip to Phase 7.

1. Ask user: "Update master briefing with new intelligence? (yes/no)"
2. If user says yes, trigger the `/intel-briefing:intel-briefing refresh` workflow internally:
   - Query new claims since last briefing
   - Dispatch `financial-analyst` and `geopolitical-analyst` agents in parallel via Task tool (run_in_background: true)
   - Collect results via TaskOutput
   - Dispatch `briefing-synthesizer` with both results
   - Store new briefing version in `rok_intel_briefings`
   - Display briefing summary
3. If user says no, note "Master briefing update skipped" and proceed

### Phase 7: Report

Display the final ingestion summary:

```
=========================================
INGESTION COMPLETE
=========================================
Document: [title]
Source: [source_type] | Author: [author] | Trust: [tier]
Classification: [classification]

Claims Extracted: [N]
  Financial: [n] | Geopolitical: [n] | Technology: [n] | Other: [n]
  Validated: [n confirmed] | [n partial] | [n unconfirmed] | [n contradicted]

Predictions Extracted: [N]
  Financial: [n] | Geopolitical: [n]

Alert Matches: [N] (list topics if any)

Master Briefing: [Updated to v[N] / Skipped]
=========================================

NEXT STEPS:
  /intel-briefing:intel-briefing            # View current master briefing
  /intel-briefing:intel-predict review      # Review predictions due for scoring
  /intel-briefing:intel-library             # Browse document library
  /intel-briefing:intel-validate            # Validate remaining unvalidated claims
```

If processing the watch folder (batch mode), show cumulative summary after all files:

```
=========================================
BATCH INGESTION COMPLETE
=========================================
Files Processed: [N] of [total]
Documents Stored: [N]
Total Claims: [N] (Financial: [n] | Geopolitical: [n] | Technology: [n] | Other: [n])
Total Predictions: [N]
Alert Matches: [N]
Master Briefing: [Updated to v[N] / Skipped]
Skipped (duplicates): [N]
Errors: [N] (list if any)
=========================================
```

## Important Rules

- ALWAYS check for duplicates via content_hash before processing
- For watch folder processing, move processed files to the `processed/` subfolder with a timestamp prefix (e.g., `2026-02-11T1430_filename.md`). Create the subfolder if it does not exist.
- Never store raw document text in Supabase -- only structured summaries and claims (raw text is too large)
- If yt-dlp fails for YouTube URLs, fall back to WebFetch page content
- Display progress to the user at each phase transition
- For MD files with YAML frontmatter, parse the frontmatter carefully -- it contains pre-curated metadata
- For TXT transcripts, strip timestamp markup and entity links during analysis but preserve the raw text for the analyst agent
- If Supabase is unreachable, warn the user and offer to save analysis to a local JSON file as fallback
- Maximum batch size for watch folder: 20 files. If more, ask user to process in batches.
- When processing watch folder batch, use `--skip-validation` per document and validate all new claims at the end for efficiency. Still offer briefing update once at the end (not per file).
