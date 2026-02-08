# Optimize Page

You are executing a single-page SEO audit for a specific URL. Your goal is to fetch the page, analyze all on-page SEO elements, score the page, and provide prioritized recommendations.

## Input

The user will provide:
- **URL** (required) — if not provided, ask for it
- **Primary keyword** (optional) — will be inferred from title/H1 if not given
- **Page type** (optional) — geo-landing, service, blog (affects scoring thresholds)

## Process

### Step 1: Fetch the Page

Use WebFetch to retrieve the page content. Extract:

1. **Title tag** — text and character count
2. **Meta description** — text and character count
3. **H1-H3 headings** — full hierarchy
4. **Canonical tag** — URL
5. **Robots meta** — directives
6. **Schema/structured data** — types present
7. **Images** — count, alt text presence
8. **Internal links** — count and anchor text samples
9. **External links** — count
10. **Word count** — total visible content words
11. **URL structure** — slug analysis

If WebFetch returns limited HTML, note which elements could not be extracted and work with what is available.

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

- Only report what you actually find — never fabricate SEO elements
- If WebFetch returns incomplete data, clearly state which checks were skipped
- Score conservatively — 90+ should be rare
- Every issue must have a specific, actionable recommendation
- Present issues sorted by severity (Critical first)
- Ask before fetching GSC data (approval gate)
- Default page type is "service" unless the URL pattern suggests otherwise (e.g., /blog/ = blog, /city-state = geo-landing)
