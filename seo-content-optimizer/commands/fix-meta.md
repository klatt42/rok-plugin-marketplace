# Fix Meta

You are analyzing and fixing the title tag and meta description of a specific URL. Your goal is to fetch the current metadata, evaluate it against best practices, generate improved versions, and present a before/after comparison.

## Input

The user will provide:
- **URL** (required) — if not provided, ask for it
- **Target keyword** (optional) — for optimization targeting
- **Brand name** (optional) — for title tag branding

## Process

### Step 1: Fetch Current Metadata

Use WebFetch to retrieve the page and extract:
- Current `<title>` tag — text and character count
- Current `<meta name="description">` — text and character count
- H1 heading — for keyword inference
- Page type — infer from URL pattern (geo-landing, service, blog)

### Step 2: Evaluate Current Metadata

**Title Tag Evaluation:**

| Check | Pass/Fail | Detail |
|-------|-----------|--------|
| Length (50-60 chars) | ✓/✗ | XX chars |
| Primary keyword present | ✓/✗ | Found/Missing |
| Keyword in first 3 words | ✓/✗ | Position X |
| Brand present | ✓/✗ | Found/Missing |
| No stuffing | ✓/✗ | X keyword variations |
| Compelling | ✓/✗ | Assessment |

**Meta Description Evaluation:**

| Check | Pass/Fail | Detail |
|-------|-----------|--------|
| Length (140-160 chars) | ✓/✗ | XX chars |
| Primary keyword present | ✓/✗ | Found/Missing |
| CTA present | ✓/✗ | Found/Missing |
| Unique value prop | ✓/✗ | Assessment |
| No stuffing | ✓/✗ | X keyword variations |

### Step 3: Generate Improved Versions

Dispatch the meta-generator agent methodology to create 3 title + 3 meta description variations based on:
- Inferred or provided primary keyword
- Page type and appropriate formula
- Brand name
- Issues identified in evaluation

### Step 4: Present Before/After

```
## Meta Fix: [URL]

### Current Title
"[current title text]" (XX chars)
Issues: [list problems found]

### Current Meta Description
"[current meta text]" (XX chars)
Issues: [list problems found]

---

### Improved Title Options
1. "[new title]" (XX chars) ✓
2. "[new title]" (XX chars) ✓
3. "[new title]" (XX chars) ✓

### Improved Meta Description Options
1. "[new meta]" (XXX chars) ✓
2. "[new meta]" (XXX chars) ✓
3. "[new meta]" (XXX chars) ✓

### Recommended Combination
**Title**: Option X — [reason]
**Meta**: Option X — [reason]

### Before → After Comparison

| Element | Before | After | Change |
|---------|--------|-------|--------|
| Title | "[old]" (XX chars) | "[new]" (XX chars) | [what improved] |
| Meta | "[old]" (XX chars) | "[new]" (XXX chars) | [what improved] |

### Copy-Ready HTML
<title>[recommended title]</title>
<meta name="description" content="[recommended meta]">
```

### Step 5: Additional Options

After presenting:
- "Fix meta for similar pages?" — batch fix for other pages with same issues
- "Export all fixes?" — spreadsheet with before/after for all pages

## Rules

- Always fetch and show the current metadata before suggesting changes
- Never exceed character limits (60 title, 160 meta)
- Always display character counts
- If current metadata is already good (passes all checks), say so and suggest only minor tweaks
- Each variation must take a genuinely different angle
- Copy-ready HTML must be pasteable directly
- Show clear before/after comparison so the user can see what changed
- If the page has no title or meta description, note this as a critical issue
