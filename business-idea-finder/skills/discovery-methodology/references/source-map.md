# Source Map — Complete Research Source Reference

## Pain Point Mining Sources

### Reddit (Primary)
**Business/Startup**:
- r/smallbusiness — General SMB pain points, tool complaints
- r/sweatystartup — Service business operators (home services heavy)
- r/microsaas — Builders sharing what niches need tools
- r/SaaS — SaaS product feedback, feature requests
- r/indiehackers — Indie builders, idea validation

**Home Services/Trades**:
- r/homeimprovement — Homeowner + contractor frustrations
- r/contractor — General contracting pain points
- r/HVAC — HVAC-specific tooling gaps
- r/plumbing — Plumbing business operations
- r/electricians — Electrical trade business tools

**Marketing/Sales**:
- r/digital_marketing — Marketing tool gaps for SMBs
- r/socialmediamarketing — Social media management pain
- r/SEO — SEO tooling for small businesses

**Insurance/Restoration**:
- r/insurancepros — Insurance industry workflow gaps
- r/restoration — Restoration industry specific

### Review Sites
- G2.com — Category pages, negative reviews for SMB tools
- Capterra — Same categories, different reviewer base
- Trustpilot — Consumer-facing tool reviews (lower signal)

### Twitter/X
- Business owner complaints: "frustrated with", "wish there was"
- Tool-specific hate threads
- "Looking for alternative to [tool]" tweets

### Protection & Safety Sources
- BBB complaints for industry-specific tools and platforms
- IC3 (Internet Crime Complaint Center) — fraud trend data
- Platform help forums (Facebook Help Community, eBay Community, etc.) — enforcement complaints
- r/Scams, r/legaladvice — fraud pattern discussions relevant to target niche
- FTC consumer complaint data — industry-level fraud statistics

### Google Search Patterns
- `"frustrated with [tool]" site:reddit.com`
- `"wish there was" OR "need a tool" [industry]`
- `"switched from" OR "looking for alternative" [category]`
- `"[industry] software sucks" OR "[industry] tools terrible"`
- `"no good [category] tool" small business 2025 OR 2026`

## Gap Analysis Sources

### Product Hunt
- Recent launches in business tool categories
- Categories with few launches (signal: underserved)
- Tools with low upvotes in validated categories (signal: room for better)

### G2/Capterra Categories
- Categories with <5 products listed
- Categories where top product is rated <4.0 stars
- Categories with "no AI" tag or no AI-powered options

### Chrome Web Store
- Business extensions with >10K installs but <3.5 stars (ripe for disruption)
- Underserved categories for business professionals
- Categories where top extension hasn't been updated in >1 year

### AppSumo
- Lifetime deal categories with repeat purchases (validated demand)
- AI tool categories with high velocity
- Business tools selling well = proven willingness to pay

### Indie Hackers
- "What I'd build next" threads
- Revenue milestone posts (validated niches)
- "I tried [category] and it sucked" complaint threads

### GitHub
- Business-focused repos with >500 stars but no SaaS wrapper
- Open source tools that could be productized

## Arbitrage Scanner Sources

### YouTube Creators (Monitored)
| Creator | Focus | Signal Type |
|---------|-------|-------------|
| Cole Medin | AI agent development, Claude Code | Technical capability signals |
| IndyDevDan | AI dev tools, agent frameworks | Tool/framework emergence |
| Mark Kashef | AI SaaS building | Business model patterns |
| Greg Isenberg | Business ideas, startup concepts | Market opportunity signals |
| Chris Koerner | Side hustles, micro-business | Validated small business models |

### Hacker News
- "Show HN" posts with AI tools (new capability signals)
- "Ask HN: What should I build?" threads
- Front page AI tool launches

### AI Tool Directories
- There's an AI for That — New category emergence
- Futurepedia — Tool launches and category trends

### API Changelogs
- OpenAI — New models, function calling, vision, assistants API
- Anthropic — Claude capabilities, computer use, tool use
- Google AI — Gemini features, AI Studio
- Smaller APIs — ElevenLabs, Replicate, Hugging Face Inference

### Twitter/X AI Community
- @levelsio — Indie hacker revenue sharing
- @marclouv — Solo SaaS builder insights
- AI developer community — New capability discussions

---

## Source Packs (Niche-Specific)

Source packs are activated via `--sources=<pack-name>` in `/find-ideas`. When active, agents APPEND these sources to their standard research sources. Default behavior (no flag or `--sources=default`) uses only the standard sources above.

### ecommerce-reseller
**Additional Reddit**: r/Flipping, r/FacebookMarketplace, r/eBaySellers, r/poshmark, r/mercari, r/Depop
**Additional communities**: Facebook Groups (search for "[platform] sellers group"), reseller YouTube channels (search comments), TikTok reseller content
**Additional review mining**: App Store / Play Store reviews for Vendoo, List Perfectly, Mercari, OfferUp, Poshmark apps — mine 1-star reviews for unmet needs
**Additional safety**: BBB complaints for marketplace platforms, IC3 marketplace fraud reports
**Search patterns**:
- `site:reddit.com r/Flipping OR r/FacebookMarketplace "[pain keyword]"`
- `"[app name]" app store review "doesn't" OR "can't" OR "wish" OR "missing"`
- `"marketplace seller" frustrated OR "wish there was" [platform]`

### home-services
**Additional Reddit**: r/HomeInspections, r/PropertyManagement, r/landscaping, r/Roofing, r/GeneralContractor
**Additional sources**: Angi/HomeAdvisor contractor forums, Thumbtack provider discussions, Nextdoor contractor threads
**Additional review mining**: G2/Capterra reviews for ServiceTitan, Housecall Pro, Jobber — mine negative reviews
**Search patterns**:
- `site:reddit.com r/contractor OR r/HVAC "[tool category]" frustrated OR "looking for"`
- `"home services" OR "field service" software "doesn't" OR "wish" OR "terrible"`

### saas-builder
**Additional Reddit**: r/webdev, r/nextjs, r/selfhosted, r/devtools, r/ChatGPTCoding
**Additional sources**: HackerNews "Ask HN: What should I build?" threads, Product Hunt trending daily, IndieHackers revenue milestones
**Additional review mining**: G2 reviews for developer tools, Vercel/Supabase community feature requests
**Search patterns**:
- `site:news.ycombinator.com "what should I build" OR "looking for tool" 2026`
- `site:reddit.com r/SaaS OR r/microsaas "wish there was" OR "someone should build"`
