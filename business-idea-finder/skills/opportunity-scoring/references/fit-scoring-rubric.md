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

## Pain Severity Scoring

### High Severity (80-100)
- "Buyer ghosting on Facebook Marketplace" — affects 100M+ marketplace users, happens daily, causes lost revenue and wasted time, no reliable workaround. Score: 95.
- "No-show appointments for home services" — affects millions of contractors daily, direct revenue loss, only workaround is double-booking. Score: 90.

### Medium Severity (40-79)
- "Scheduling conflicts across multiple booking platforms" — affects thousands of multi-platform sellers weekly, workaround exists (manual calendar sync) but is tedious. Score: 60.
- "Inconsistent pricing across marketplace listings" — affects sellers on 2+ platforms, workaround is spreadsheets. Score: 55.

### Low Severity (0-39)
- "Aesthetic inconsistency in listing photos" — minor annoyance, affects presentation not revenue. Score: 20.
- "Lack of emoji support in business messaging tools" — cosmetic preference, doesn't block any workflow. Score: 10.

## TAM Estimation Examples

### Large TAM ($100M+)
- "Facebook Marketplace seller tools" — 1B+ marketplace users globally, even 1% power sellers (10M) at $10/mo = $1.2B TAM. Estimate: $100M+ (conservative, US-focused segment).

### Medium TAM ($10-100M)
- "AI estimating tool for restoration contractors" — ~50,000 restoration companies in US, $50/mo willingness-to-pay = $30M TAM.

### Small TAM ($1-10M)
- "Chrome extension for HVAC permit lookup" — ~100,000 HVAC companies in US, $10/mo, 10% addressable = $1.2M TAM.

### Insufficient Data
- "AI tool for niche regulatory compliance" — Cannot estimate without knowing target sub-industry size. Use "unknown" and explain the gap.

## Defensibility Assessment Examples

### High Defensibility
- "Community-sourced contractor reputation platform" — Network effects: value increases with each user, data moat from aggregated reviews, high switching costs once reputation is established.
- "AI model trained on proprietary industry data" — Data moat: model improves with usage, competitors can't replicate training data.

### Medium Defensibility
- "AI-powered CRM with industry-specific templates" — Domain expertise moat: deep understanding of restoration/home services workflows. Competitors could build but would take 6-12 months to match depth.
- "Tool with crowdsourced pricing data" — Partial data moat: community contributions create value but could be replicated with enough investment.

### Low Defensibility
- "Chrome extension wrapping a public API" — No proprietary data, minimal switching costs. Platform (Chrome) could add the feature natively.
- "Simple automation connecting two SaaS tools" — Zapier/Make could add this as a template. Speed-to-market is the only advantage.

## Network Potential Classification Examples

### Single-User
- "AI listing description generator" — Each user gets value independently, no network needed.
- "Automated repricing tool" — Works for one seller in isolation.

### Network-Optional
- "Contractor scheduling tool with customer portal" — Core value is single-user (scheduling), but customer-facing portal adds network-like value.
- "Marketplace analytics dashboard with benchmarking" — Works alone, but community data makes benchmarks better.

### Network-Required
- "Buyer/seller reputation verification across platforms" — Meaningless without a critical mass of users contributing reputation data.
- "Marketplace for connecting sub-contractors" — Two-sided marketplace, inherently requires network.
