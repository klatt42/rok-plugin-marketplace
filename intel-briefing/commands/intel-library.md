# /intel-library - Browse Document Library

Browse, search, and get statistics on the ingested document library. View all documents that have been processed by the intelligence system with their metadata, claim counts, and trust assessments.

## Usage

```
/intel-briefing:intel-library                       # Show recent 20 documents
/intel-briefing:intel-library search:"gold"         # Full-text search in titles and summaries
/intel-briefing:intel-library source_type:youtube    # Filter by source type
/intel-briefing:intel-library source_type:markdown   # Filter by markdown sources
/intel-briefing:intel-library author:"Peter Schiff"  # Filter by author
/intel-briefing:intel-library since:2026-01-01      # Filter by ingest date
/intel-briefing:intel-library stats                 # Show comprehensive statistics
/intel-briefing:intel-library document:[uuid]       # Show full details for a specific document
```

### Parameters
- **search** - Search term to match against document titles and summaries (case-insensitive)
- **source_type** - Filter by type: `youtube`, `url`, `pdf`, `markdown`, `text`, `article`
- **author** - Filter by author name (partial match)
- **since** - Only show documents ingested after this date (ISO format YYYY-MM-DD)
- **stats** - Show aggregate statistics instead of document list
- **document** - UUID of a specific document for detailed view
- **limit** - Number of documents to show (default 20, max 100)

Initial request: $ARGUMENTS

## Execution Steps

### Mode: Recent Documents (default, no special args)

1. Query recent documents from Supabase:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?order=ingest_date.desc&limit=20&select=id,source_type,title,author,ingest_date,trust_tier,classification,topics,word_count" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. For each document, get claim and prediction counts:
   ```bash
   # Claims per document (batch query)
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?document_id=in.(${DOC_IDS})&select=document_id,id" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

   # Predictions per document (batch query)
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?document_id=in.(${DOC_IDS})&select=document_id,id" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

3. Display formatted list:
   ```
   DOCUMENT LIBRARY (Recent 20)
   =========================================

   # | Title                          | Type     | Author          | Date       | Trust    | Claims | Predictions
   --|--------------------------------|----------|-----------------|------------|----------|--------|------------
   1 | [title]                        | [type]   | [author]        | [date]     | [tier]   | [n]    | [n]
   2 | [title]                        | [type]   | [author]        | [date]     | [tier]   | [n]    | [n]
   ...

   Total Documents: [N] | Showing: [displayed]

   COMMANDS:
     /intel-briefing:intel-library document:[id]     # View full details
     /intel-briefing:intel-library search:"topic"    # Search documents
     /intel-briefing:intel-library stats              # View statistics
   ```

### Mode: Search (if "search:" is present)

1. Query documents matching the search term:
   ```bash
   # Search in title
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?or=(title.ilike.%25${TERM}%25,raw_summary.ilike.%25${TERM}%25)&order=ingest_date.desc&limit=20&select=id,source_type,title,author,ingest_date,trust_tier,classification,topics,raw_summary" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Also search in claims for the term:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?claim_text=ilike.%25${TERM}%25&select=id,document_id,claim_text,category,validation_status&limit=10" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

3. Display results:
   ```
   SEARCH RESULTS: "[term]"
   =========================================

   Documents Matching ([N]):
   # | Title                          | Type     | Author          | Relevance
   --|--------------------------------|----------|-----------------|----------
   1 | [title]                        | [type]   | [author]        | [title match / summary match]
   ...

   Claims Matching ([N]):
   # | Claim                                    | Category    | Status        | Document
   --|------------------------------------------|-------------|---------------|----------
   1 | [claim_text excerpt]                     | [category]  | [val_status]  | [doc_title]
   ...
   ```

### Mode: Filtered List (if source_type, author, or since provided)

1. Build query with applied filters:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?[filters]&order=ingest_date.desc&limit=${LIMIT}&select=id,source_type,title,author,ingest_date,trust_tier,classification,topics,word_count" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

   Filters:
   - `source_type:youtube` adds `&source_type=eq.youtube`
   - `author:"Name"` adds `&author=ilike.%25Name%25`
   - `since:2026-01-01` adds `&ingest_date=gte.2026-01-01`

2. Display using same table format as default mode, with filter noted in header

### Mode: Document Detail (if "document:" is present)

1. Query the specific document:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?id=eq.${DOC_ID}&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Query all claims for this document:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?document_id=eq.${DOC_ID}&order=confidence_score.desc&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

3. Query all predictions for this document:
   ```bash
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?document_id=eq.${DOC_ID}&order=created_at.desc&select=*" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

4. Display full detail view:
   ```
   =========================================
   DOCUMENT DETAIL
   =========================================
   Title: [title]
   ID: [uuid]
   Source Type: [type] | Classification: [classification]
   Author: [author] | Trust Tier: [tier]
   Ingested: [ingest_date] | Published: [publish_date]
   Word Count: [count]
   URL: [source_url or N/A]
   Topics: [topic1, topic2, ...]
   Tags: [tag1, tag2, ...]

   Summary:
   [raw_summary text]

   Claims ([N]):
   -----------------------------------------
   [1] "[claim_text]"
       Category: [category] ([subcategory]) | Type: [claim_type]
       Confidence: [score] | Validation: [status]
       Tags: [tags]

   [2] "[claim_text]"
       ...

   Predictions ([N]):
   -----------------------------------------
   [1] "[prediction_text]"
       Category: [category] | Timeframe: [timeframe]
       Confidence: [initial] -> [current] | Target: [target_date]
       Outcome: [outcome]

   [2] "[prediction_text]"
       ...
   =========================================
   ```

### Mode: Statistics (if "stats")

1. Query aggregate data:
   ```bash
   # All documents
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_documents?select=id,source_type,author,ingest_date,trust_tier,topics" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

   # All claims with categories
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_claims?select=id,category,validation_status,claim_type" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

   # All predictions with outcomes
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_predictions?select=id,category,outcome" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

   # Source registry
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_sources?order=documents_analyzed.desc&select=source_name,trust_tier,documents_analyzed,prediction_accuracy" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

   # Briefing count
   curl -s "${ROK_SUPABASE_URL}/rest/v1/rok_intel_briefings?select=version&order=version.desc&limit=1" \
     -H "apikey: ${ROK_SUPABASE_KEY}" \
     -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
   ```

2. Calculate and display statistics:
   ```
   =========================================
   INTELLIGENCE LIBRARY STATISTICS
   =========================================

   Documents
   ---------
   Total: [N]
   By Type:
     YouTube:  [n] | Markdown: [n] | Text: [n]
     URL:      [n] | PDF:      [n] | Article: [n]
   Date Range: [earliest] to [latest]

   Trust Distribution:
     HIGH:     [n] | MEDIUM:   [n] | STANDARD: [n]

   Top Authors (by document count):
   | Author              | Documents | Trust Tier |
   |---------------------|-----------|------------|
   | [author]            | [n]       | [tier]     |
   | [author]            | [n]       | [tier]     |
   | ...                 |           |            |

   Most Common Topics:
   | Topic               | Documents |
   |---------------------|-----------|
   | [topic]             | [n]       |
   | [topic]             | [n]       |
   | ...                 |           |

   Claims
   ------
   Total: [N]
   By Category:
     Financial: [n] | Geopolitical: [n] | Technology: [n]
     Economic:  [n] | Market:       [n] | Policy:     [n]
     Military:  [n] | Social:       [n] | Energy:     [n]
     Labor:     [n] | Other:        [n]
   By Validation:
     Confirmed: [n] | Partial: [n] | Unconfirmed: [n]
     Contradicted: [n] | Unvalidated: [n]

   Predictions
   -----------
   Total: [N]
   By Outcome:
     Pending: [n] | Correct: [n] | Partial: [n]
     Incorrect: [n] | Indeterminate: [n]

   Briefings
   ---------
   Total Versions: [N]
   Latest: v[N] ([date])

   =========================================
   ```

## Important Rules

- Always show claim count and prediction count per document in list views
- For stats mode, include trust tier distribution across documents
- When displaying document summaries, truncate to first 200 characters with "..." if longer
- Search is case-insensitive using Supabase `ilike` operator
- Limit results to prevent overwhelming output (default 20, respect user limit up to 100)
- If Supabase returns empty results, display helpful messages pointing to ingestion
- For document detail view, show full information including all claims and predictions
- Topic frequency is calculated by flattening the topics array across all documents and counting occurrences
