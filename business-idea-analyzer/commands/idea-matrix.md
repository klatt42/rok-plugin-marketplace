# Idea Matrix

Quick comparative scoring matrix for 2-5 business ideas side-by-side. This is a LIGHTWEIGHT command -- no subagents, no export files, just WebSearch queries and a comparison table displayed in chat.

## Usage

```
/business-idea-analyzer:idea-matrix "AI photo editor" vs "AI video editor" vs "AI audio editor"
/business-idea-analyzer:idea-matrix "Shopify analytics app" vs "eBay listing tool" --depth=quick
/business-idea-analyzer:idea-matrix "meal prep SaaS" vs "fitness tracker" vs "recipe marketplace" vs "nutrition coaching platform"
```

### Arguments

- **idea descriptions** (required): 2-5 business ideas separated by `vs`. Each idea can be quoted or unquoted.
- **--depth** (optional): `quick` (2-3 searches per idea, ~2 min) or `standard` (default, 3-5 searches per idea, ~5 min).

Initial request: $ARGUMENTS

## Process

### Step 1: Parse Ideas

Split the input on `vs` (case-insensitive). Trim whitespace and remove surrounding quotes from each idea.

Validation:
- If fewer than 2 ideas found, ask: "Please provide at least 2 ideas separated by 'vs' to compare."
- If more than 5 ideas found, ask: "Maximum 5 ideas for comparison. Please narrow your list."

Extract the `--depth` flag if present. Default: `standard`.

### Step 2: Research Each Idea

For each idea, run WebSearch queries to gather scoring signals:

**Quick depth** (2-3 queries per idea):
- `"[idea keywords]" market demand OR users OR growth`
- `"[idea keywords]" competitor OR alternative OR tool`
- `"[idea keywords]" pricing OR revenue OR business model`

**Standard depth** (3-5 queries per idea):
- `"[idea keywords]" market size OR demand OR trend 2025 2026`
- `"[idea keywords]" competitor OR alternative OR existing tool`
- `"[idea keywords]" pricing OR monetization OR revenue model`
- `"[idea keywords]" build OR MVP OR technical feasibility`
- `"[idea keywords]" risk OR challenge OR barrier`

Capture key signals from each search for scoring in Step 3.

### Step 3: Score Each Idea

For each idea, assign a score (0-100) across 5 dimensions based on the research signals:

| Dimension | Weight | What to Evaluate |
|-----------|--------|-------------------|
| Market Demand | 0.25 | Search volume, user complaints, unmet needs, growing trends |
| Competitive Landscape | 0.20 | Number of competitors, gaps in existing solutions, defensibility |
| Financial Viability | 0.20 | Willingness to pay, pricing benchmarks, revenue potential |
| Execution Feasibility | 0.20 | Technical complexity, time to MVP, solopreneur viability |
| Risk Assessment | 0.15 | Platform dependency, regulatory, market timing, technical risk |

Calculate composite score:
```
weighted = (demand * 0.25) + (competitive * 0.20) + (financial * 0.20) + (execution * 0.20) + (risk * 0.15)
final = round(weighted)
```

### Step 4: Determine Verdicts

| Score Range | Verdict |
|-------------|---------|
| >= 80 | STRONG_GO |
| 65-79 | GO |
| 50-64 | CONDITIONAL |
| < 50 | NO_GO |

### Step 5: Display Comparison Table

Present the matrix in chat:

```markdown
## Idea Comparison Matrix

**Date:** [YYYY-MM-DD] | **Depth:** [quick/standard] | **Ideas compared:** [N]

| Dimension (Weight) | [Idea 1] | [Idea 2] | [Idea 3] |
|---------------------|----------|----------|----------|
| Market Demand (25%) | XX | XX | XX |
| Competitive Landscape (20%) | XX | XX | XX |
| Financial Viability (20%) | XX | XX | XX |
| Execution Feasibility (20%) | XX | XX | XX |
| Risk Assessment (15%) | XX | XX | XX |
| **Composite Score** | **XX** | **XX** | **XX** |
| **Verdict** | GO | CONDITIONAL | NO_GO |

### Key Differentiators

- **[Idea 1]**: [1-2 sentence summary of strongest signal]
- **[Idea 2]**: [1-2 sentence summary]
- **[Idea 3]**: [1-2 sentence summary]

### Recommendation

[1-2 sentences: which idea ranks highest and why. If scores are close, note that a deeper analysis is warranted.]

### Next Steps
- Deep dive on the top idea: `/business-idea-analyzer:idea-deep-dive [top idea]`
- Full analysis with agents: `/business-idea-analyzer:analyze-idea [top idea]`
- Validate assumptions: `/business-idea-analyzer:idea-validate [top idea]`
```

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All scoring must be grounded in WebSearch results. Do not fabricate data or statistics.
- If a search returns no useful results for a dimension, assign a score of 50 and note "insufficient data."
- Confidence threshold: if fewer than 2 searches return useful results for an idea, flag it as "low confidence."
- Do not launch subagents. This command runs entirely in the main thread.
- Do not write export files. Output is chat-only.
