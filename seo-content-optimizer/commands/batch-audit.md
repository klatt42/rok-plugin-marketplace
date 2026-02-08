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

### Step 4: Execute Audit (Two-Phase Extraction)

**IMPORTANT**: WebFetch converts HTML to markdown, which strips `<head>` meta tags. For accurate audits, you MUST use curl to extract `<head>` elements from raw HTML.

#### Extraction Method

For each URL, use a **two-phase approach**:

1. **Phase 1 (curl)**: Fetch raw HTML `<head>` to extract title, meta description, canonical, robots, OG tags, Twitter cards, favicon, schema types
   ```bash
   curl -sL -A "Mozilla/5.0 (compatible; SEOBot/1.0)" "[URL]" | sed -n '/<head/,/<\/head>/p' | head -100
   ```
2. **Phase 2 (WebFetch)**: Fetch page for body content — headings (H1-H3), word count, links, images, content structure

For **batch efficiency**, you can run multiple curl commands in a single Bash call (one per URL), then use WebFetch for body content as needed per depth level.

If curl and WebFetch disagree on any element, **always trust curl (raw HTML)**.

Rate limit: 1-2 seconds between requests.

#### Depth Levels

**Quick audit** extracts (curl only — fastest):
- Title tag (text + length)
- Meta description (text + length)
- H1 (from curl `<head>` is not reliable for H1 — use a quick WebFetch or grep from curl body)
- Canonical tag presence
- Robots meta presence
- Score: based on these technical elements

**Standard audit** extracts (curl + WebFetch per page):
- All HTML SEO elements from `<head>` (Phase 1)
- Body content analysis from WebFetch (Phase 2)
- Content analysis (word count, structure)
- Keyword density for inferred primary keyword
- Internal/external link counts
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
- **Always use curl (raw HTML) as the authoritative source for `<head>` meta tags** — never rely on WebFetch alone for meta description, canonical, OG tags, Twitter cards, or robots meta
- Rate limit: 1-2 seconds between requests to avoid overwhelming servers
- If a URL fails to fetch via curl, try WebFetch as fallback; log failures and continue
- Display progress during execution
- Sort priority pages by score ascending (worst first)
- For deep audits, ask for GSC approval separately
- Max batch size: 100 URLs per run (suggest splitting larger sets)
- If sitemap contains >100 URLs, present count and ask user to filter or confirm
