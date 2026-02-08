---
name: onpage-seo
description: |
  On-page SEO evaluation methodology for landing pages. Covers title tag rules
  (50-60 chars), meta description (140-160 chars), heading hierarchy, content
  structure, internal linking, technical requirements, and Core Web Vitals.
  Includes geo-landing page specific rules for city+service pages, scoring
  methodology across 5 categories, and common issues checklist with severity.
triggers:
  - "optimize page"
  - "seo audit"
  - "page optimization"
  - "title tag"
  - "meta description"
  - "internal linking"
  - "technical seo"
version: 1.0
author: ROK Agency
---

# On-Page SEO Evaluation

## Title Tag Rules

| Rule | Requirement | Severity |
|------|-------------|----------|
| Length | 50-60 characters (hard limit 60) | Critical |
| Primary keyword | Within first 3 words | High |
| Brand | Append ` | Brand Name` at end | Medium |
| Uniqueness | No two pages share same title | Critical |
| No stuffing | Max 2 keyword variations | High |
| Compelling | Action-oriented or benefit-driven | Medium |

### Geo-Landing Title Formula
```
[Service] in [City], [State] | [Brand]
```
Example: `Water Damage Restoration in Arlington, VA | Prism Specialties`

### Service Page Title Formula
```
[Primary Service] Services | [Brand]
```

### Blog Post Title Formula
```
[Topic]: [Benefit or How-to] | [Brand]
```

## Meta Description Rules

| Rule | Requirement | Severity |
|------|-------------|----------|
| Length | 140-160 characters (hard limit 160) | Critical |
| Primary keyword | Include naturally once | High |
| CTA | Include call-to-action (call, contact, learn more) | Medium |
| Uniqueness | No two pages share same description | Critical |
| Value prop | Communicate unique benefit | Medium |
| No truncation | Preview in SERP before publishing | Low |

## Heading Hierarchy

| Rule | Requirement | Severity |
|------|-------------|----------|
| H1 count | Exactly one per page | Critical |
| H1 keyword | Contains primary keyword | High |
| H2 structure | 3-8 H2s per page for content pages | Medium |
| No skipping | H1 > H2 > H3 (no H1 > H3 jumps) | Medium |
| H2 keywords | Include secondary keywords naturally | Medium |

## Content Structure

| Element | Minimum | Target | Severity |
|---------|---------|--------|----------|
| Word count (service page) | 500 | 800-1200 | High |
| Word count (geo page) | 300 | 500-800 | High |
| Word count (blog post) | 800 | 1500-2500 | Medium |
| Paragraphs | 3+ | 5-10 | Medium |
| Keyword in first 100 words | Required | — | High |
| Image alt text | All images | Descriptive + keyword where natural | Medium |

## Internal Linking

| Rule | Requirement | Severity |
|------|-------------|----------|
| Links per page | 3-10 internal links | High |
| Anchor text | Descriptive, keyword-rich (no "click here") | Medium |
| Link to parent | Service pages link to category | Medium |
| Cross-link siblings | Related service pages interlink | Medium |
| Orphan pages | Every page reachable from nav or links | High |
| Broken links | Zero tolerance | Critical |

## Technical Requirements

| Element | Requirement | Severity |
|---------|-------------|----------|
| Canonical tag | Self-referencing on every page | Critical |
| Robots meta | No accidental noindex | Critical |
| Schema markup | LocalBusiness for geo pages, Service for service pages | Medium |
| Mobile responsive | Passes mobile-friendly test | High |
| Page speed | LCP < 2.5s, FID < 100ms, CLS < 0.1 | High |
| HTTPS | Required | Critical |
| URL structure | Lowercase, hyphens, keyword in slug | Medium |
| Sitemap | Page included in XML sitemap | Medium |

## Geo-Landing Page Specific Rules

| Rule | Requirement | Severity |
|------|-------------|----------|
| Unique content | Min 60% unique vs other geo pages | Critical |
| City name | In title, H1, first paragraph, URL | High |
| Local signals | Address, phone, service area mention | High |
| NAP consistency | Name, Address, Phone match GMB | Critical |
| Local schema | LocalBusiness with geo coordinates | Medium |
| Nearby areas | Mention 2-3 nearby cities/neighborhoods | Medium |
| Local testimonial | Include if available | Low |

## Common Issues Checklist

| Issue | Severity | Detection |
|-------|----------|-----------|
| Missing title tag | Critical | Empty or absent `<title>` |
| Duplicate title | Critical | Same title on multiple pages |
| Title too long (>60) | High | Character count |
| Title too short (<30) | Medium | Character count |
| Missing meta description | Critical | Empty or absent meta description |
| Duplicate meta description | Critical | Same description on multiple pages |
| Meta too long (>160) | High | Character count |
| Missing H1 | Critical | No `<h1>` element |
| Multiple H1s | High | More than one `<h1>` |
| Missing canonical | Critical | No canonical tag |
| Noindex on indexed page | Critical | Robots meta or header |
| Thin content (<300 words) | High | Word count |
| No internal links | High | Zero outbound internal links |
| Missing alt text | Medium | Images without alt attribute |
| Broken internal links | Critical | 404 responses |
| Missing schema | Medium | No structured data |
| Non-HTTPS resources | High | Mixed content |
| Missing sitemap entry | Medium | Not in XML sitemap |

## Scoring Methodology

**Total Score: 0-100** (weighted average)

| Category | Weight | Factors |
|----------|--------|---------|
| Technical | 25% | Canonical, robots, HTTPS, schema, speed |
| Content | 25% | Word count, structure, readability, uniqueness |
| Keywords | 20% | Title placement, density, H1, meta |
| Linking | 15% | Internal links, anchors, orphans, broken |
| UX | 15% | Mobile, speed, CLS, accessibility |

### Score Ranges

| Range | Label | Color |
|-------|-------|-------|
| 90-100 | Excellent | Green |
| 80-89 | Good | Light Green |
| 70-79 | Needs Work | Yellow |
| 60-69 | Poor | Orange |
| 0-59 | Critical | Red |

### Severity Impact on Score

| Severity | Point Deduction |
|----------|----------------|
| Critical | -15 per issue |
| High | -8 per issue |
| Medium | -4 per issue |
| Low | -2 per issue |
