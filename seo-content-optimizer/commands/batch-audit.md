# Batch Audit

You are executing a batch SEO audit across multiple pages. Your goal is to efficiently audit an inventory of URLs, aggregate findings, and produce a comprehensive report.

## Input

The user will provide one of:
- **Sitemap URL** — XML sitemap to fetch and parse for URLs
- **File path** — local file containing one URL per line
- **Manual list** — URLs provided directly in chat
- **Saved inventory** — reference to a previously audited set

Optional filters:
- **Page type filter**: all, service, geo, blog, custom regex
- **Audit depth**: quick, standard, deep

## Process

### Step 1: Collect URLs

**From sitemap**:
1. Use WebFetch to retrieve the sitemap XML
2. Extract all `<loc>` URLs
3. If sitemap index, list sub-sitemaps and ask which to audit

**From file**: Read the file at the given path, one URL per line.

**From manual list**: Parse URLs from the user's message.

Apply filters if specified:
- Service pages: URLs matching `/services/` or similar patterns
- Geo pages: URLs matching `/city-state/` or `/locations/` patterns
- Blog: URLs matching `/blog/` or `/news/`
- Custom regex: user-provided pattern

### Step 2: Configure Depth

| Depth | What's Checked | Approx Time/Page |
|-------|---------------|-------------------|
| Quick | Title, meta description, H1 only | ~2s |
| Standard | All on-page elements, content, links | ~5s |
| Deep | Standard + GSC data pull | ~15s |

Default: **standard**

### Step 3: APPROVAL GATE

**STOP and present the audit plan before proceeding.**

```
## Batch Audit Plan

- Pages to audit: [X]
- Audit depth: [quick/standard/deep]
- Filter applied: [description or "none"]
- Rate limiting: 1-2 sec between requests

Sample URLs:
1. [first 5 URLs listed]
...

Proceed with audit?
```

**Wait for explicit user confirmation.** Do not begin fetching pages without approval.

### Step 4: Execute Audit

For each URL, use WebFetch with 1-2 second delays between requests:

**Quick audit** extracts:
- Title tag (text + length)
- Meta description (text + length)
- H1 (text + count)
- Score: based on these 3 elements only

**Standard audit** extracts (full page-analyzer methodology):
- All HTML SEO elements
- Content analysis (word count, structure)
- Keyword density for inferred primary keyword
- Internal/external link counts
- Technical checks (canonical, robots, schema)
- Score: weighted across all 5 categories

**Deep audit** adds:
- GSC page analytics (requires approval for first GSC call)
- Ranking queries and positions
- CTR analysis

Display progress:
```
Auditing: [X/Total] [URL] ... Score: XX
```

### Step 5: Aggregate Results

After all pages are audited, compile:

```
## Batch Audit Summary

### Overview
- Pages audited: XX
- Average score: XX/100
- Score distribution: XX excellent, XX good, XX needs work, XX poor, XX critical

### Issues by Severity
- Critical: XX issues across XX pages
- High: XX issues across XX pages
- Medium: XX issues across XX pages
- Low: XX issues across XX pages

### Most Common Issues
1. [Issue] — found on XX pages (XX%)
2. [Issue] — found on XX pages (XX%)
3. [Issue] — found on XX pages (XX%)

### Priority Pages (score < 70)
| URL | Score | Critical Issues | Top Issue |
|-----|-------|----------------|-----------|
| ... | XX | X | [description] |

### Score Distribution
| Range | Count | Pages |
|-------|-------|-------|
| 90-100 (Excellent) | X | [urls] |
| 80-89 (Good) | X | [urls] |
| 70-79 (Needs Work) | X | [urls] |
| 60-69 (Poor) | X | [urls] |
| 0-59 (Critical) | X | [urls] |
```

### Step 6: Export

Offer export options:
- **Chat summary** — already displayed above
- **Full Excel** — all page scores + all issues + recommendations (4 sheets)
- **Issues Excel** — issues-only export for task assignment
- **PDF executive summary** — score distribution, top issues, priority pages

If the user chooses to export, dispatch the report-generator agent with the full batch data to construct the `type: "seo_audit"` payload and run `prospecting_export.py`.

## Rules

- Always present the APPROVAL GATE before starting
- Rate limit: 1-2 seconds between WebFetch calls to avoid overwhelming servers
- If a URL fails to fetch, log it and continue (don't stop the batch)
- Display progress during execution
- Sort priority pages by score ascending (worst first)
- For deep audits, ask for GSC approval separately
- Max batch size: 100 URLs per run (suggest splitting larger sets)
- If sitemap contains >100 URLs, present count and ask user to filter or confirm
