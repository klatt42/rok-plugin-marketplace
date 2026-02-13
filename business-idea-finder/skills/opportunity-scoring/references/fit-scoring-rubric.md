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

### Arbitrage Window Calibration (for Market Demand — recency signal)
- "Just became possible this month" (new API release): 90-100
- "Possible for <6 months": 70-85
- "Possible for 6-12 months but no one's built it": 50-70
- "Possible for >1 year, competitors emerging": 20-40
- "Has existed for years, market saturated": 0-15

### Time to Commoditization Calibration (for Competitive Durability — inverse of window)
- "2+ years before replication" (data moat, network effects): 90-100
- "12-18 months" (domain expertise + integration lock-in): 70-85
- "6-12 months" (moderate switching costs): 50-70
- "3-6 months" (speed-only advantage, competitors closing in): 20-40
- "Already commoditized" (multiple competitors, no moat): 0-15

### Moat Type Examples
- **Data network effects**: Buyer reputation platform — each user's reviews make the platform more valuable. Score: 90-100.
- **Switching costs**: CRM with years of customer data — switching loses history. Score: 70-85.
- **Integration lock-in**: Tool deeply embedded in seller workflow, connects to 5+ other tools. Score: 75-90.
- **Community**: Crowdsourced pricing data — users contribute, creating shared value. Score: 60-80.
- **Speed-only**: First mover with no proprietary data or network. Score: 10-25.
- **None**: API wrapper, no data retention, trivially replaceable. Score: 0-10.

## Build Estimate Tiers

### Tier Definitions
- **MVP** (2-4 weeks): Proof of concept. Core feature only, no auth/billing, basic UI. Enough to validate demand.
- **Beta** (6-10 weeks): Feature-complete beta. Auth, basic billing, reasonable UI, initial user testing. Not production-hardened.
- **Production** (12-20 weeks): Production-grade. Full billing integration, error handling, monitoring, docs, Chrome Web Store review (if extension), proper QA.

### Hidden Complexity Flags
| Flag | What It Means | Impact |
|------|--------------|--------|
| `chrome_extension_review` | Chrome Web Store review process (2-4 weeks, may require revisions) | Adds 2-6 weeks to beta/production timelines |
| `platform_scraping` | Relies on scraping a platform's DOM/pages | High maintenance — DOM changes break the tool |
| `anti_bot_risk` | Platform actively blocks automated access | May require constant workarounds, legal risk |
| `ai_prompt_engineering` | Core value depends on prompt quality/tuning | Iterative tuning adds 1-2 weeks per prompt chain |
| `model_costs` | AI inference costs affect unit economics | Must validate cost-per-user before scaling |
| `dom_dependency` | Chrome extension touches third-party DOM | Breaks when target site updates, ongoing maintenance |
| `auth_billing_integration` | Requires user auth + payment processing | Adds 2-4 weeks minimum for Stripe/auth setup |

### Maintenance Profile
- **low**: Standalone SaaS, no external dependencies. Quarterly updates sufficient.
- **medium**: API-dependent, moderate external integrations. Monthly checks needed.
- **high**: DOM-scraping Chrome extension or platform-dependent tool. Weekly monitoring, frequent patches.

### Examples
- "AI listing description generator (SaaS)": MVP 1-2wk, Beta 4-6wk, Production 8-12wk. Hidden: `ai_prompt_engineering`. Maintenance: low.
- "Chrome extension for Facebook Marketplace CRM": MVP 2-4wk, Beta 8-12wk, Production 16-24wk. Hidden: `chrome_extension_review`, `dom_dependency`, `auth_billing_integration`. Maintenance: high.
- "Price comparison API service": MVP 2-3wk, Beta 6-8wk, Production 10-14wk. Hidden: `platform_scraping`, `anti_bot_risk`. Maintenance: medium.

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

## Ecosystem Score Examples

### High Ecosystem Value (80-100)
- "CRM for marketplace sellers" — Generates buyer interaction data that feeds analytics, pricing, and fraud detection tools. Natural wedge product that drives adoption of an entire seller toolkit. Score: 90.
- "Analytics dashboard for seller performance" — Consumes data from listing tools, pricing tools, and messaging tools. Becomes the hub of a seller's daily workflow. Score: 85.

### Medium Ecosystem Value (40-79)
- "Profit calculator for resellers" — Generates cost/margin data useful for pricing tools, but limited cross-tool value beyond that. Score: 55.
- "AI pricing intelligence tool" — Feeds into listing tools and analytics, moderate data generation value. Score: 65.

### Low Ecosystem Value (0-39)
- "AI Agent Orchestrator for workflow automation" — Generic standalone tool, doesn't generate niche-specific data, no natural adjacency to other seller tools. Score: 15.
- "One-click relisting tool" — Solves a narrow task, minimal data generation, low integration surface area. Score: 25.

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
