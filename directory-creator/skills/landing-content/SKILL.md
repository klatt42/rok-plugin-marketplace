---
name: landing-content
description: |
  SEO content generation patterns for directory landing pages.
  Covers title tag formulas, meta description templates, schema
  markup for LocalBusiness and ItemList, content style options
  (authority, local-seo, lead-gen, minimal), and FAQ generation.
  Used by the content-generator agent and generate-landing-content command.
triggers:
  - "landing content"
  - "directory landing page"
  - "directory SEO"
version: 1.0
author: ROK Agency
---

# Directory Landing Page Content

## SEO Best Practices

### Title Tag Formulas (50-60 chars)
1. `[N] Best [Niche] in [City], [ST] | [Directory Name]`
2. `Top [Niche] in [City] - [N] Verified Pros | [Name]`
3. `[City] [Niche] Directory - [N] Rated & Reviewed`
4. `Find [Niche] Near [City], [ST] | [N] Listed`

### Meta Description Templates (140-160 chars)
1. `Compare [N] verified [niche] in [city], [ST]. Read reviews, check ratings, and find trusted [niche keyword] near you.`
2. `Browse [N] [niche] serving [geography]. Verified ratings, hours, and contact info. Find the right [niche pro] today.`
3. `[City]'s most complete [niche] directory. [N] businesses with reviews, ratings, and verified contact information.`

### Schema Markup

**ItemList** (for the directory page):
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "[Directory Name]",
  "description": "[Meta description]",
  "numberOfItems": [N],
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "item": {
        "@type": "LocalBusiness",
        "name": "[Business Name]",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "[Address]",
          "addressLocality": "[City]",
          "addressRegion": "[State]",
          "postalCode": "[Zip]"
        },
        "telephone": "[Phone]",
        "url": "[Website]",
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "[Rating]",
          "reviewCount": "[ReviewCount]"
        }
      }
    }
  ]
}
```

## Content Style Guide

### Authority Style
- Tone: Professional, data-driven, trustworthy
- Perspective: Third-person ("This directory provides...")
- Evidence: Cite verification process, data sources, coverage stats
- Length: Full sections, comprehensive FAQs

### Local-SEO Style
- Tone: Warm, community-focused
- Perspective: Second-person ("Find your local...")
- Localization: Mention neighborhoods, landmarks, local events
- Length: Standard, with hyper-local keywords woven in

### Lead-Gen Style
- Tone: Action-oriented, urgent
- Perspective: Second-person imperative ("Get quotes now")
- CTAs: Every section has a call to action
- Length: Moderate, focused on conversion

### Minimal Style
- Tone: Clean, direct
- Perspective: Neutral
- Content: Essential info only, no fluff
- Length: Short sections, 3-4 FAQs max

## FAQ Generation Guidelines

Always include these universal FAQs:
1. "How do I find the best [niche] in [geography]?"
2. "Are these [niche] businesses verified?"
3. "How often is this directory updated?"

Add 2-4 niche-specific FAQs based on common consumer questions:
- Home services: costs, licensing, emergency availability
- Legal: specializations, free consultations, case types
- Medical: insurance acceptance, appointment availability
- Food: dietary options, delivery, reservations
- Auto: warranty, certification, specializations
