# Optimize Page

You are executing a single-page SEO audit for a specific URL. Your goal is to fetch the page, analyze all on-page SEO elements, score the page, and provide prioritized recommendations.

## Input

The user will provide:
- **URL** (required) — if not provided, ask for it
- **Primary keyword** (optional) — will be inferred from title/H1 if not given
- **Page type** (optional) — geo-landing, service, blog (affects scoring thresholds)

## Process

### Step 1: Fetch the Page (Two-Phase Extraction)

**IMPORTANT**: WebFetch converts HTML to markdown, which strips `<head>` meta tags. You MUST use both extraction methods for accurate results.

#### Phase 1: Raw HTML `<head>` Extraction (via curl)

Use Bash to run `curl` and extract all `<head>` meta tags from the raw HTML source. This is the **authoritative source** for technical SEO elements:

```bash
curl -sL -A "Mozilla/5.0 (compatible; SEOBot/1.0)" "[URL]" | sed -n '/<head/,/<\/head>/p' | head -100
```

From the raw `<head>` HTML, extract:
1. **Title tag** — `<title>` text and character count
2. **Meta description** — `<meta name="description">` content and character count
3. **Canonical tag** — `<link rel="canonical">` href value
4. **Robots meta** — `<meta name="robots">` directives
5. **Open Graph tags** — all `<meta property="og:*">` tags
6. **Twitter Card tags** — all `<meta name="twitter:*">` tags
7. **Favicon** — `<link rel="icon">` presence
8. **Schema/structured data** — `<script type="application/ld+json">` types

If curl returns a redirect or incomplete response, follow the redirect URL and retry.

#### Phase 2: Body Content Analysis (via WebFetch)

Use WebFetch to retrieve the page for body content analysis:
1. **H1-H3 headings** — full hierarchy, count of each level
2. **Images** — count, alt text presence
3. **Internal links** — count and anchor text samples
4. **External links** — count
5. **Word count** — total visible content words
6. **URL structure** — slug analysis
7. **Content quality** — paragraph structure, readability

#### Merging Results

Combine Phase 1 and Phase 2 data. If there is a conflict between curl (Phase 1) and WebFetch (Phase 2) for any element, **always trust the curl/raw HTML result** — WebFetch's markdown conversion drops `<head>` content.

### Step 2: Keyword Analysis

Determine the primary keyword (from user input, title, or H1) and check:

- **Density**: Count occurrences, calculate percentage against total words
- **Placement**: Title, H1, first 100 words, URL, meta description, H2s, alt text
- **Variations**: Identify related terms and their density
- **Stuffing check**: Flag if primary >3% or combined >10%

### Step 3: Score the Page

Apply the onpage-seo skill scoring methodology:

| Category | Weight | What to Check |
|----------|--------|---------------|
| Technical (25%) | Canonical, robots, HTTPS, schema, URL structure |
| Content (25%) | Word count, headings, paragraphs, readability |
| Keywords (20%) | Density, placement, title optimization |
| Linking (15%) | Internal link count, anchor text quality |
| UX (15%) | Content structure, image alt text, mobile indicators |

Deductions per issue: Critical -15, High -8, Medium -4, Low -2

### Step 4: GSC Data (Optional)

If Google Search Console MCP tools are available:

**APPROVAL GATE**: "I can pull GSC performance data for this URL. This will show impressions, clicks, CTR, and ranking queries. Should I fetch GSC data?"

Wait for user confirmation before calling GSC tools.

If approved, use `gsc_page_analytics` to get:
- Top queries driving impressions
- Click-through rate
- Average position
- Compare ranking keywords to on-page optimization

### Step 5: Present Results

Display a comprehensive scorecard:

```
## SEO Audit: [URL]

### Overall Score: [XX]/100

| Category | Score | Status |
|----------|-------|--------|
| Technical | XX/100 | ✓/⚠/✗ |
| Content | XX/100 | ✓/⚠/✗ |
| Keywords | XX/100 | ✓/⚠/✗ |
| Linking | XX/100 | ✓/⚠/✗ |
| UX | XX/100 | ✓/⚠/✗ |

### Current Elements
- Title: "[title text]" (XX chars)
- Meta: "[meta text]" (XX chars)
- H1: "[h1 text]"
- Word Count: XXX
- Internal Links: XX
- Schema: [types or "None"]

### Issues Found (sorted by severity)

**Critical**
- [issue description] → [specific fix]

**High**
- [issue description] → [specific fix]

**Medium**
- [issue description] → [specific fix]

**Low**
- [issue description] → [specific fix]

### Opportunities
- [actionable improvement suggestion]
```

### Step 6: Export Options

After presenting the scorecard, offer:

"Would you like to export this audit?"
- **Chat only** — already displayed above
- **PDF** — professional PDF scorecard
- **Excel** — spreadsheet with scores and issues
- **All** — both PDF and Excel

If the user chooses to export, dispatch the report-generator agent to construct the `type: "seo_audit"` JSON payload and run `prospecting_export.py`.

## Rules

- **Always use curl (Phase 1) as the authoritative source for `<head>` elements** — never rely on WebFetch alone for meta tags, canonical, OG, or Twitter cards
- Only report what you actually find — never fabricate SEO elements
- If curl returns incomplete data (e.g., JS-rendered pages), note this limitation and try WebFetch as fallback
- Score conservatively — 90+ should be rare
- Every issue must have a specific, actionable recommendation
- Present issues sorted by severity (Critical first)
- Ask before fetching GSC data (approval gate)
- Default page type is "service" unless the URL pattern suggests otherwise (e.g., /blog/ = blog, /city-state = geo-landing)
