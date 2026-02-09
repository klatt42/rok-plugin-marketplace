# Fit Scoring Rubric — Examples and Edge Cases

## Profile Fit Examples

### High Fit (80-100)
- "AI-powered job estimating assistant for restoration contractors" — Domain expertise (restoration), picks-and-shovels (tool for contractors), AI-first, buildable as Chrome extension or SaaS. Score: 95.
- "Chrome extension that auto-generates social media posts from project photos for home services businesses" — Domain match, familiar tech (extension), AI-powered, clear solopreneur build. Score: 90.

### Medium Fit (50-79)
- "AI scheduling optimizer for field service teams" — Domain adjacent (home services), but scheduling is a crowded space. Build complexity is medium — needs calendar integrations. Score: 65.
- "Automated compliance document generator for small businesses" — Picks-and-shovels, but domain expertise is less relevant (generic compliance, not restoration-specific). Score: 60.

### Low Fit (0-49)
- "AI personal shopping assistant" — Consumer app (exclusion), no domain advantage, wrong audience. Score: 15.
- "Marketplace for connecting homeowners with contractors" — Marketplace model is complex, borderline consumer app, not picks-and-shovels. Score: 35.

## Opportunity Signal Examples

### Strong Signal (80-100)
- Reddit thread with 200+ upvotes: "Why is there no good estimating tool for small restoration companies?" + G2 showing the only tools are enterprise ($500/mo+) + Anthropic just released vision API improvements. Score: 92.

### Medium Signal (50-79)
- 2 Reddit complaints about insurance documentation being tedious + 1 AppSumo tool in the space selling well but poorly rated. Score: 65.

### Weak Signal (0-49)
- A single tweet from someone saying "someone should build X" + saturated competitive landscape. Score: 25.

## Edge Cases

### Borderline Exclusions
- "AI-powered product listing optimizer for Amazon sellers" — E-commerce adjacent, but the TOOL itself is picks-and-shovels. Exclusion check: 40 (borderline), not 0. Let the composite score decide.
- "Real estate CRM with AI follow-up" — Real estate exclusion, but CRM is a tool. Exclusion check: 20 (closer to excluded).

### Domain Advantage Interpretation
- Direct match (home services, restoration, insurance): 80-100
- Adjacent (construction, property management, field services): 50-70
- Tangential (general SMB operations, marketing): 30-50
- None (healthcare, education, fintech): 0-20

### Arbitrage Window Calibration
- "Just became possible this month" (new API release): 90-100
- "Possible for <6 months": 70-85
- "Possible for 6-12 months but no one's built it": 50-70
- "Possible for >1 year, competitors emerging": 20-40
- "Has existed for years, market saturated": 0-15
