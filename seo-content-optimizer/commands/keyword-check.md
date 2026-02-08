# Keyword Check

You are performing a keyword analysis on a specific URL. Your goal is to fetch the page, analyze keyword density and placement, detect over/under-optimization, and report findings with a score.

## Input

The user will provide:
- **URL** (required) — if not provided, ask for it
- **Target keyword** (optional) — will be inferred from title/H1 if not given
- **Comparison URLs** (optional) — for cannibalization detection

## Process

### Step 1: Fetch the Page

Use WebFetch to retrieve the page. Extract:
- Title tag text
- Meta description text
- H1 text
- H2 texts (all)
- Visible body text content
- Image alt texts
- URL slug
- First 100 words
- Last paragraph

### Step 2: Determine Target Keyword

If the user provided a target keyword, use it. Otherwise:
1. Extract the title tag
2. Extract the H1
3. Identify the most prominent 2-4 word phrase that appears in both
4. Present the inferred keyword: "I'm analyzing for the keyword **[keyword]** — is this correct?"
5. Proceed unless the user corrects it

### Step 3: Calculate Density

Count occurrences of:
- **Primary keyword** (exact match)
- **Primary variations** (plural, gerund, reordered)
- **Secondary keywords** (other prominent 2-3 word phrases)

Calculate:
```
Density = (occurrences / total_words) * 100
```

Evaluate against targets:

| Type | Optimal | Warning | Over-optimized |
|------|---------|---------|----------------|
| Primary | 1.0-2.5% | 2.5-3.0% | >3.0% |
| Secondary | 0.5-1.5% | 1.5-2.0% | >2.0% |
| Combined | 4-8% | 8-10% | >10% |

### Step 4: Check Placement

Check primary keyword presence in each location:

| Location | Weight | Found? |
|----------|--------|--------|
| Title tag | 5x | ✓/✗ |
| H1 | 4x | ✓/✗ |
| First 100 words | 3x | ✓/✗ |
| URL slug | 3x | ✓/✗ |
| Meta description | 2x | ✓/✗ |
| H2 headings (2+) | 2x | X found |
| Image alt text | 1x | ✓/✗ |
| Last paragraph | 1x | ✓/✗ |

Calculate placement score: `(found_weights / total_weights) * 100`

### Step 5: Cannibalization Check (if comparison URLs provided)

If the user provided multiple URLs:
1. Fetch each comparison URL
2. Extract their target keywords (from title/H1)
3. Compare keyword overlap with the primary URL
4. Flag pages with >70% keyword overlap
5. Check for identical titles or meta descriptions

### Step 6: Present Results

```
## Keyword Analysis: [URL]

### Target Keyword: "[primary keyword]"

### Density Analysis
| Keyword | Count | Total Words | Density | Status |
|---------|-------|-------------|---------|--------|
| [primary] | X | XXX | X.X% | optimal/low/high |
| [variation 1] | X | XXX | X.X% | ... |
| [secondary 1] | X | XXX | X.X% | ... |
| **Combined** | XX | XXX | X.X% | ... |

### Placement Check
| Location | Status | Detail |
|----------|--------|--------|
| Title tag | ✓/✗ | "[title text]" |
| H1 | ✓/✗ | "[h1 text]" |
| First 100 words | ✓/✗ | Found at word position X |
| URL slug | ✓/✗ | /[slug] |
| Meta description | ✓/✗ | "[meta text]" |
| H2 headings | X/Y | [which H2s contain keyword] |
| Image alt text | ✓/✗ | [which images] |
| Last paragraph | ✓/✗ | Found/Not found |

**Placement Score: XX/100**

### Issues
- [Over/under-optimization flags]
- [Missing placements]
- [Stuffing warnings]

### Keyword Score: XX/100

### Recommendations
1. [Specific actionable fix for each issue]
```

## Rules

- Base all counts on actual page content — never fabricate numbers
- If primary keyword cannot be determined, ask the user
- Count both exact matches and close variations separately
- Clearly flag both over-optimization (stuffing) and under-optimization
- For cannibalization, only analyze if comparison URLs are explicitly provided
- Every issue must have a specific recommendation
- Show the actual text found at each placement location for verification
