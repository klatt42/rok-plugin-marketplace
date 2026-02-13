---
name: marketization-pathways
description: |
  Framework for evaluating plugin-to-product transitions.
  Six pathways: SaaS App, Chrome Extension, API Service,
  Marketplace Plugin, Mobile App, Hybrid. Includes revenue
  models, build estimates, and real examples from the portfolio.
triggers:
  - "marketize plugin"
  - "plugin to product"
  - "product pathway"
version: 1.0
author: ROK Agency
---

# Marketization Pathways

## Philosophy

"Build for yourself first, marketize if valuable."

A Claude Code plugin is a rapid prototyping vehicle. The plugin validates the concept, the product pathway describes how to package it for others.

## Pathway Types

### 1. SaaS App (`saas_app`)

**What**: Web application with subscription billing.
**Stack**: Next.js + Supabase + Stripe + Vercel
**Revenue**: Monthly/annual subscriptions, tiered pricing
**Build delta**: Plugin → SaaS typically adds 4-8 weeks (auth, billing, multi-tenancy, UI)

**Best for**: Tools that need persistent data, user accounts, team features, or dashboards.

**Transition steps**:
1. Extract core logic from plugin agents into API routes
2. Build Next.js frontend with auth (Supabase Auth)
3. Add Stripe billing (3 tiers recommended)
4. Deploy to Vercel
5. Add onboarding flow and documentation

### 2. Chrome Extension (`chrome_extension`)

**What**: Browser-native tool distributed via Chrome Web Store.
**Stack**: Manifest V3, TypeScript, React (popup/sidebar)
**Revenue**: Freemium + premium features, or one-time purchase
**Build delta**: Plugin → Extension typically adds 2-4 weeks (UI, manifest, store listing)

**Best for**: Tools that enhance web browsing, interact with specific websites, or need real-time page context.

**Transition steps**:
1. Identify which plugin logic runs on page content vs. background
2. Build popup/sidebar UI with React
3. Implement Manifest V3 service worker
4. Add licensing (Gumroad or self-hosted)
5. Chrome Web Store submission (1-2 week review)

### 3. API Service (`api_service`)

**What**: Expose plugin capabilities as a consumable API.
**Stack**: Python FastAPI or Next.js API routes + rate limiting
**Revenue**: Usage-based pricing, API key tiers
**Build delta**: Plugin → API typically adds 2-3 weeks (auth, rate limiting, docs)

**Best for**: Tools whose output is data/analysis that other developers would integrate into their own apps.

**Transition steps**:
1. Define API schema from plugin output format
2. Build REST or GraphQL endpoints
3. Add API key auth and rate limiting
4. Generate OpenAPI docs
5. Deploy to Vercel/Railway

### 4. Marketplace Plugin (`marketplace_plugin`)

**What**: Stays in the Claude Code plugin ecosystem, distributed through marketplace.
**Stack**: Same as plugin (agents, commands, skills)
**Revenue**: Free (reputation), freemium, or plugin marketplace fees
**Build delta**: Minimal — polish, docs, testing

**Best for**: Tools that are inherently CLI/agent-first and most valuable inside Claude Code.

**Transition steps**:
1. Clean up agent instructions for general users
2. Remove hardcoded paths and operator-specific config
3. Add configuration system for user customization
4. Write README and usage docs
5. Publish to marketplace

### 5. Mobile App (`mobile_app`)

**What**: Mobile-first product.
**Stack**: React Native or Expo
**Revenue**: App Store subscription or in-app purchases
**Build delta**: Plugin → Mobile typically adds 8-12 weeks (new platform)

**Best for**: Tools that need mobile-first UX, push notifications, or offline access.

**Note**: This pathway has the highest build delta and is least aligned with the operator's core stack.

### 6. Hybrid (`hybrid`)

**What**: Multiple pathways are viable simultaneously.
**Example**: Plugin + Chrome Extension + SaaS dashboard all sharing the same backend.
**Revenue**: Multiple revenue streams

**Best for**: Tools with multiple user touchpoints (CLI users + browser users + dashboard users).

## Revenue Model Guidance

| Pathway | Recommended Model | Typical Price Range |
|---------|------------------|---------------------|
| SaaS App | Tiered subscription | $19-99/mo |
| Chrome Extension | Freemium or one-time | $0-49 one-time, or $5-15/mo |
| API Service | Usage-based | $0.01-0.10/request, or $29-99/mo tiers |
| Marketplace Plugin | Free or freemium | $0-29/mo |
| Mobile App | Subscription | $4.99-14.99/mo |
| Hybrid | Mixed | Varies by channel |

## Reference Documents

- `references/pathway-examples.md` — Real examples from the portfolio
