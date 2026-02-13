# Pathway Examples — Real Portfolio Transitions

## Example 1: seo-content-optimizer → SaaS App

**Plugin**: Analyzes on-page SEO, generates meta tags, checks keyword density
**Product**: SaaS with Stripe billing for agencies

**Transition**:
- Core: Page analysis agents become API endpoints
- Frontend: Next.js dashboard with URL input, history, team sharing
- Billing: 3 tiers — Solo ($29/mo, 50 audits), Agency ($79/mo, 500 audits), Enterprise ($199/mo, unlimited)
- Value add: Batch auditing, competitor tracking, weekly email reports
- TAM: SEO agencies and freelancers ($5-10B SEO tools market)

**Pathway**: `saas_app`
**Build delta**: ~6 weeks from plugin to production SaaS

---

## Example 2: production-code-review → VS Code Extension / GitHub Action

**Plugin**: 6-agent comprehensive code review (security, performance, UI/UX, responsive, code quality, tests)
**Product**: VS Code extension or GitHub Action

**Transition (VS Code Extension)**:
- Core: Review agents become extension commands triggered on file save or PR
- Frontend: VS Code sidebar panel showing findings inline
- Billing: Free tier (1 review/day), Pro ($15/mo, unlimited)
- Value add: Auto-fix suggestions, team configuration, CI integration

**Transition (GitHub Action)**:
- Core: Run review agents as GitHub Action on PR creation
- Output: PR comments with findings, severity labels
- Billing: Free for public repos, $10/mo for private
- Value add: Configurable rules, ignore patterns, team standards

**Pathway**: `hybrid` (VS Code + GitHub Action)
**Build delta**: ~4 weeks for VS Code, ~3 weeks for GitHub Action

---

## Example 3: vehicle-recommender → Consumer Web App

**Plugin**: Researches vehicles based on user requirements across 5 dimensions
**Product**: Consumer web app with affiliate revenue

**Transition**:
- Core: Research agents become background jobs, results cached in Supabase
- Frontend: Guided wizard UI (budget, needs, preferences → ranked recommendations)
- Revenue: Affiliate links to dealership partners, lead gen fees
- Value add: Price alerts, market timing advice, comparison tools
- TAM: Car buyers in US (~15M/year, $1-5B in referral/lead gen market)

**Pathway**: `saas_app` (freemium + affiliate)
**Build delta**: ~8 weeks including dealer partnership integrations

---

## Example 4: intel-briefing → Newsletter / Paid Research

**Plugin**: Multi-source intelligence synthesis with prediction tracking
**Product**: Paid newsletter or research subscription

**Transition**:
- Core: Document analysis + synthesis agents run on schedule
- Output: Weekly HTML email briefings
- Distribution: Substack, Beehiiv, or self-hosted
- Revenue: Paid subscription $15-30/mo, or bundled with consulting
- Value add: Prediction scorecard, historical accuracy tracking

**Pathway**: `saas_app` (content subscription variant)
**Build delta**: ~3 weeks for automated pipeline + subscription management

---

## Example 5: business-idea-finder → Web App for Indie Hackers

**Plugin**: Multi-agent business opportunity discovery with scoring
**Product**: SaaS for indie hackers and solopreneurs

**Transition**:
- Core: Research agents become background workers with queue system
- Frontend: Dashboard showing idea shortlists, saved searches, trend alerts
- Billing: Free (1 scan/week), Pro ($39/mo, daily scans + deep mode), Team ($99/mo)
- Value add: Community-sourced validation data, idea marketplace, co-founder matching
- TAM: Indie hackers, solopreneurs (~500K active globally, growing)

**Pathway**: `saas_app`
**Build delta**: ~8 weeks including worker queue and community features

---

## Example 6: campaign-management → Chrome Extension

**Plugin**: Email campaign scoring, optimization, and A/B testing
**Product**: Chrome extension for email marketers

**Transition**:
- Core: Message scorer runs on email compose in Gmail/Outlook
- Frontend: Sidebar panel with real-time scoring as you type
- Billing: Freemium — 5 scores/day free, $9.99/mo unlimited
- Distribution: Chrome Web Store
- Value add: Template library, A/B test suggestions, send-time optimization

**Pathway**: `chrome_extension`
**Build delta**: ~4 weeks including Gmail API integration

---

## Transition Complexity Guide

| From Plugin Feature | To Product Feature | Typical Effort |
|--------------------|--------------------|----------------|
| Agent research logic | API endpoint | 1-2 days |
| JSON output schema | Database schema | 1 day |
| CLI display template | React dashboard | 3-5 days |
| File-based export | Stripe billing + email delivery | 3-5 days |
| Hardcoded profile | User configuration system | 2-3 days |
| Local file storage | Supabase tables + RLS | 2-3 days |
| Single-user plugin | Multi-tenant SaaS | 5-10 days |
| WebSearch research | Scheduled background jobs | 3-5 days |
