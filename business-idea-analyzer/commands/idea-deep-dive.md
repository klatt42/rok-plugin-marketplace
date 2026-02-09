# Idea Deep Dive

Produces PRD-level analysis for a single business opportunity. This is a deeper, single-agent exploration designed to produce output that feeds directly into `/2_plan` or `/create-prd` workflows. No subagents are launched -- all research runs sequentially in the main thread with extensive WebSearch.

## Usage

```
/business-idea-analyzer:idea-deep-dive AI-powered inventory management for eBay sellers
/business-idea-analyzer:idea-deep-dive --source="Seller Analytics Dashboard"
/business-idea-analyzer:idea-deep-dive Chrome extension for Amazon price tracking --focus=solopreneur
```

### Arguments

- **idea description** (required unless `--source` provided): The business opportunity to deep-dive.
- **--source** (optional): Name of an opportunity from a previous `/analyze-idea` session. Loads context from that analysis instead of starting fresh.
- **--focus** (optional): `solopreneur` (default) or `enterprise`. Adjusts pricing tiers and GTM strategy.

Initial request: $ARGUMENTS

## Process

### Step 1: Establish Context

**If `--source` provided:**
- Look for the named opportunity in the current session's analysis data (from a prior `/analyze-idea` run).
- Extract the existing scores, findings, and signals as a starting point.
- If not found in session, ask: "I don't have analysis data for '[source name]' in this session. Please provide the idea description directly, or run `/analyze-idea` first."

**If new idea description provided:**
- Run 3-5 WebSearch queries to build initial context:
  - `"[idea keywords]" market OR industry OR users`
  - `"[idea keywords]" competitor OR tool OR platform`
  - `"[idea keywords]" pain points OR problems OR gaps`
  - `"[idea keywords]" pricing OR revenue OR business model`
  - `"[idea keywords]" trend OR growth 2025 2026`

Present a brief context summary and confirm with the user before proceeding.

### Step 2: Competitive Feature Matrix

Search for 5-10 direct competitors or adjacent solutions:
- `"[idea keywords]" competitor OR alternative OR similar tool`
- `"[idea keywords]" vs OR comparison OR review`
- `best [idea category] tools 2025 2026`

Build a detailed feature comparison table:

```markdown
### Competitive Feature Matrix

| Feature | [Comp 1] | [Comp 2] | [Comp 3] | [Comp 4] | [Comp 5] | **Proposed** |
|---------|----------|----------|----------|----------|----------|-------------|
| [Feature 1] | Yes | Yes | No | Yes | No | **Yes** |
| [Feature 2] | No | Yes | Yes | No | No | **Yes** |
| Pricing | $X/mo | $Y/mo | Free | $Z/mo | $W/mo | **TBD** |
| Free Tier | Yes | No | Yes | No | Yes | **Yes** |

**Key Gaps Identified:** [2-3 bullet points on what competitors miss]
```

### Step 3: Pain Point Severity Analysis

Search for user complaints and unmet needs:
- `"[idea keywords]" frustrated OR annoying OR wish OR "pain point"`
- `"[idea keywords]" site:reddit.com OR site:quora.com`
- `"[idea keywords]" review OR complaint OR limitation`

Build a prioritized pain point table:

```markdown
### Pain Point Severity Analysis

| # | Pain Point | Severity (0-100) | Frequency | Affected Segment | Economic Impact |
|---|-----------|-------------------|-----------|------------------|-----------------|
| 1 | [Description] | 92 | Daily | [Segment] | $X/mo lost per user |
| 2 | [Description] | 85 | Weekly | [Segment] | $Y/mo inefficiency |
```

Identify the top 10 pain points. Each must be specific and evidence-backed (cite the search source).

### Step 4: MVP Feature Specification

Based on the competitive matrix and pain points, define the MVP:

```markdown
### MVP Feature Specification

**Core Features (Must-Have for Launch)**:
1. [Feature] -- addresses pain point #X, competitive gap
2. [Feature] -- addresses pain point #Y
3. [Feature] -- table stakes (all competitors have this)

**Nice-to-Have (Post-Launch Sprint 2-3)**:
1. [Feature] -- differentiator but not launch-critical
2. [Feature] -- requested by segment Z

**Future Features (Roadmap V2+)**:
1. [Feature] -- requires scale to justify
2. [Feature] -- adjacent market expansion

**Estimated MVP Timeline:** [X-Y weeks] for a solo developer
**Tech Stack Recommendation:** [Based on idea category and feasibility]
```

### Step 5: Pricing Tier Analysis

Research competitor pricing models:
- `"[idea keywords]" pricing OR plans OR cost`
- `"[competitor names]" pricing page`

Recommend a 3-tier pricing structure:

```markdown
### Pricing Tier Analysis

**Competitor Pricing Range:** $X - $Y/mo

| Tier | Price | Target User | Key Features | Limits |
|------|-------|-------------|-------------|--------|
| Free | $0/mo | Trial / hobby users | [Core feature subset] | [Usage caps] |
| Pro | $XX/mo | Power users / small biz | [Full features] | [Higher limits] |
| Business | $XX/mo | Teams / agencies | [Pro + team features] | [Unlimited or high] |

**Pricing Rationale:** [2-3 sentences: why this structure, anchored to competitor data]
**Revenue Target:** [Y1 projection based on user estimates and conversion assumptions]
```

### Step 6: Go-to-Market Strategy

Define a phased GTM plan:

```markdown
### Go-to-Market Strategy

**Phase 1: Beta (Months 0-3)**
- Channels: [Specific communities, subreddits, forums]
- Strategy: Free beta, collect feedback, iterate on core features
- Target: 50-100 active users
- Key metric: Daily active usage rate
- Budget: $0-100/mo (organic only)

**Phase 2: Paid Acquisition (Months 3-6)**
- Channels: [Content marketing, SEO, paid ads if warranted]
- Strategy: Launch free tier publicly, start Pro conversions
- Target: 200-500 users, 5-10% paid conversion
- Key metric: MRR and churn rate
- Budget: $200-500/mo

**Phase 3: Scale (Months 6-12)**
- Channels: [Partnerships, integrations, referral program]
- Strategy: Business tier launch, partnership deals, affiliate program
- Target: 1,000+ users, 8-12% paid conversion
- Key metric: Net revenue retention
- Budget: [% of MRR]

**Phase 4: Expansion (Months 12-24)**
- Channels: [Adjacent markets, enterprise sales, API/platform]
- Strategy: Expand feature set, enter adjacent verticals, API access
- Target: 5,000+ users
- Key metric: LTV:CAC ratio > 3:1
- Budget: [% of MRR]
```

### Step 7: Build First Recommendations

Synthesize everything into the top 5 things to build, ordered by impact:

```markdown
### "Build First" Recommendations

1. **[Specific Feature/Component]** -- [Why first: addresses top pain point, competitive gap, etc.]
   - Effort: [X days/weeks]
   - Validates: [Which assumption it tests]

2. **[Specific Feature/Component]** -- [Why second]
   - Effort: [X days/weeks]
   - Validates: [Which assumption]

3. **[Specific Feature/Component]** -- [Why third]
   - Effort: [X days/weeks]
   - Validates: [Which assumption]

4. **[Specific Feature/Component]** -- [Why fourth]
   - Effort: [X days/weeks]
   - Validates: [Which assumption]

5. **[Specific Feature/Component]** -- [Why fifth]
   - Effort: [X days/weeks]
   - Validates: [Which assumption]
```

### Step 8: Present Full Report

Display the complete deep-dive in chat. The output format is designed to be compatible with `/2_plan` research-input format, so the user can proceed directly to planning.

```markdown
### Next Steps
- Validate assumptions: `/business-idea-analyzer:idea-validate [idea]`
- Export to files: `/business-idea-analyzer:idea-export`
- Start planning: `/2_plan` (reference this deep-dive output)
- Compare with alternatives: `/business-idea-analyzer:idea-matrix [idea] vs [alt1] vs [alt2]`
```

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All data must come from WebSearch. Do not fabricate statistics, pricing, or competitor information.
- If a competitor's pricing page is not accessible, note "pricing not publicly available" rather than guessing.
- Every pain point must cite evidence from search results.
- Pricing recommendations must be anchored to real competitor pricing data.
- GTM user targets should be realistic for a solopreneur operator unless `--focus=enterprise`.
- Output stays in chat. The user can run `/idea-export` separately to generate files.
- Do not launch subagents. All research runs in the main thread.
