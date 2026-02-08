# Generate Meta

You are generating optimized title tags and meta descriptions. Your goal is to produce 3 variations of each, validate them against best practices, and provide copy-ready HTML output.

## Input

The user will provide:
- **Topic or service+location** (required) — e.g., "water damage restoration Arlington VA"
- **Brand name** (optional) — default: use from context or ask
- **Page type** (optional) — geo-landing, service, blog (affects formula)
- **Current title/meta** (optional) — for improvement comparison

If not enough context is provided, ask: "What service and location is this page for? And what brand name should I use?"

## Process

### Step 1: Determine Page Type and Formula

| Page Type | Title Formula | Meta Formula |
|-----------|--------------|--------------|
| Geo-landing | `[Service] in [City], [State] \| [Brand]` | `[Service] in [City]? [Benefit]. [Proof]. [CTA].` |
| Service | `[Service] Services - [Benefit] \| [Brand]` | `Professional [service] from [brand]. [Differentiator]. [CTA].` |
| Blog | `[Topic]: [Benefit/How-to] \| [Brand]` | `Learn [topic]. [Takeaway]. [CTA].` |

### Step 2: Generate 3 Title Variations

Each variation should take a different angle:
1. **Standard** — straightforward formula application
2. **Benefit-focused** — emphasize value proposition
3. **Action-oriented** — urgency or action words

Rules:
- 50-60 characters (hard max 60)
- Primary keyword in first 3 words
- Brand name at end after pipe separator
- No keyword stuffing (max 2 keyword variations)
- Display character count for each

### Step 3: Generate 3 Meta Description Variations

Each variation should take a different angle:
1. **Benefit + CTA** — lead with what the customer gets
2. **Social proof + CTA** — certifications, experience, reviews
3. **Urgency + CTA** — emergency, fast response, availability

Rules:
- 140-160 characters (hard max 160)
- Primary keyword included naturally
- Call-to-action in every variation
- No keyword stuffing
- Display character count for each

### Step 4: Quality Validation

For each generated element, check:
- [ ] Within character limits
- [ ] Primary keyword present
- [ ] No stuffing (max 2 keyword variations per element)
- [ ] Reads naturally
- [ ] Compelling — would generate clicks
- [ ] CTA present (meta descriptions)
- [ ] Brand present (titles)

Flag any issues with warnings.

### Step 5: Present Results

```
## Title Tag Options

1. "[title text]" (XX chars) ✓
2. "[title text]" (XX chars) ✓
3. "[title text]" (XX chars) ✓

## Meta Description Options

1. "[meta text]" (XXX chars) ✓
2. "[meta text]" (XXX chars) ✓
3. "[meta text]" (XXX chars) ✓

## Recommended Combination
**Title**: Option X — [reason]
**Meta**: Option X — [reason]

## Copy-Ready HTML
<title>[recommended title]</title>
<meta name="description" content="[recommended meta]">
```

### Step 6: Additional Options

After presenting, offer:
- "Generate for similar pages?" — batch generate for other city+service combinations
- "Export to spreadsheet?" — create Excel with all variations for multiple pages
- "Compare with current?" — if current meta was provided, show before/after

If batch generation is requested, generate title+meta for each page and compile into a table, then offer Excel export via the report-generator agent.

## Rules

- Never exceed character limits (60 title, 160 meta)
- Always show character counts
- Flag any option that is at or over the limit
- Primary keyword must appear in all variations
- Each variation must take a genuinely different angle
- Recommend the best combination with clear reasoning
- Copy-ready HTML must be pasteable directly into page source
- For geo-landing pages, always include the city name
