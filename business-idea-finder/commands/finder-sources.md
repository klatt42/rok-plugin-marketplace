# Finder Sources — Research Source Reference

Display the configured research sources, search patterns, and operator profile for each discovery mode. Reference command — no research is performed.

## Usage

```
/business-idea-finder:finder-sources                    # Show all modes
/business-idea-finder:finder-sources --mode=arbitrage   # Show single mode detail
```

## Arguments

- **--mode** (optional): `pain-points`, `gaps`, `arbitrage`, or `all` (default: `all`)

Initial request: $ARGUMENTS

## Workflow

Display the following reference information:

### Operator Profile
```
OPERATOR PROFILE
================
Builder: Solopreneur, AI-first, Claude Code
Stack: Next.js, Supabase, Chrome extensions, Python, AI APIs
Domain: Home services, restoration, SMB operations, insurance
Focus: Micro-SaaS, AI tools, picks-and-shovels
Timeline: <4 week MVP, Q2 2026 launch
Excluded: E-commerce, dropshipping, real estate, rentals, investments, consumer apps
```

### Pain Point Mining Sources
| Source | Targets | Search Patterns |
|--------|---------|-----------------|
| Reddit | r/smallbusiness, r/sweatystartup, r/microsaas, r/SaaS, r/indiehackers, r/homeimprovement, r/contractor, r/HVAC, r/plumbing, r/electricians, r/digital_marketing, r/insurancepros, r/restoration | `"[pain]" site:reddit.com`, `"wish there was"`, `"frustrated with"` |
| Review sites | G2, Capterra, Trustpilot | Negative reviews for SMB tools |
| Twitter/X | Business owner complaints | `"wish there was a tool"`, `"hate using"` |
| Google | General search | `"no good [category] tool"`, `"[industry] software sucks"` |

### Gap Analysis Sources
| Source | Targets | Search Patterns |
|--------|---------|-----------------|
| Product Hunt | Recent launches, missing categories | `site:producthunt.com "[category]" 2025 2026` |
| G2/Capterra | Category pages for SMB tools | Low-rated categories, few options |
| Chrome Web Store | Business extensions | High installs + bad reviews |
| AppSumo | Lifetime deal tools | Validated demand categories |
| Indie Hackers | Success stories | "What I'd build next" threads |
| GitHub | Popular business repos | Repos without SaaS wrappers |

### Arbitrage Scanner Sources
| Source | Targets | Search Patterns |
|--------|---------|-----------------|
| YouTube | Cole Medin, IndyDevDan, Mark Kashef, Greg Isenberg, Chris Koerner | `site:youtube.com "[creator]" build OR idea 2026` |
| Hacker News | Show HN, Ask HN | `site:news.ycombinator.com "Show HN" AI [category]` |
| AI directories | There's an AI for That, Futurepedia | Newly launched AI tools |
| API changelogs | OpenAI, Anthropic, Google AI | New capabilities and announcements |
| Twitter/X AI | @levelsio, @marclouv, indie hackers | Revenue sharing, new launches |

### Scoring Rubric Summary
**Profile Fit (60%)**: Build complexity (25%), Tech stack match (20%), Domain advantage (20%), Picks-and-shovels (20%), Exclusion check (15%)

**Opportunity Signal (40%)**: Pain evidence (30%), Competition gap (25%), Arbitrage window (20%), Monetization clarity (15%), Market size (10%)

**Tiers**: HOT (>=80) | WARM (65-79) | WATCH (50-64) | PASS (<50)

## Rules
- This is a reference-only command. No searches, no research, no scoring.
- Show only the requested mode if `--mode` is specified.
