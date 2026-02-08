---
name: keyword-analysis
description: |
  Keyword density analysis, placement checking, and cannibalization detection
  for SEO content. Includes density target ranges (1.0-2.5% primary),
  placement priority mapping across title/H1/meta/body, keyword variation
  patterns for restoration services, and geo-keyword patterns for city+service
  pages. Detects over-optimization and cannibalization across page inventories.
triggers:
  - "keyword density"
  - "keyword analysis"
  - "keyword check"
  - "cannibalization"
  - "keyword stuffing"
version: 1.0
author: ROK Agency
---

# Keyword Analysis

## Density Targets

| Keyword Type | Target Range | Over-Optimized |
|-------------|-------------|----------------|
| Primary keyword | 1.0-2.5% | >3.0% |
| Secondary keywords | 0.5-1.5% each | >2.0% each |
| LSI / related terms | 0.3-0.8% each | >1.5% each |
| Total keyword footprint | 4-8% combined | >10% combined |

### Calculating Density
```
Density = (keyword occurrences / total words) * 100
```

Count both exact match and close variations (plural, gerund).

## Placement Priority

| Location | Priority | Weight | Check |
|----------|----------|--------|-------|
| Title tag | Critical | 5x | Primary keyword in first 3 words |
| H1 | Critical | 4x | Primary keyword present |
| First 100 words | High | 3x | Primary keyword in opening paragraph |
| URL slug | High | 3x | Primary keyword in URL |
| Meta description | High | 2x | Primary keyword included |
| H2 headings | Medium | 2x | Secondary keywords in 2+ H2s |
| Image alt text | Medium | 1x | Keyword in at least one alt |
| Last paragraph | Low | 1x | Keyword mention in closing |

### Placement Score
```
Score = Sum(found_placements * weight) / Sum(all_weights) * 100
```

## Keyword Variation Patterns

### Restoration Services

| Primary | Variations |
|---------|-----------|
| water damage restoration | water damage repair, water damage cleanup, water mitigation, flood damage restoration |
| mold remediation | mold removal, mold cleanup, mold mitigation, mold inspection, mold testing |
| fire damage restoration | fire damage repair, fire cleanup, smoke damage restoration, fire mitigation |
| storm damage restoration | storm damage repair, wind damage, hail damage, storm cleanup |
| contents restoration | contents cleaning, contents pack-out, contents storage, personal property restoration |
| commercial restoration | commercial water damage, commercial fire damage, commercial mold |

### Service Modifiers

| Modifier Type | Examples |
|---------------|----------|
| Emergency | emergency, 24/7, same-day, immediate, urgent |
| Geographic | [city], [county], [state], near me, local |
| Quality | certified, licensed, professional, experienced, IICRC |
| Action | services, company, contractor, specialist, expert |

## Geo-Keyword Patterns

### City+Service Page Formula
```
Primary: [service] in [city] [state]
Secondary: [city] [service] company
Tertiary: [service] near [neighborhood/area]
```

### Example for Arlington VA Water Damage Page
```
Primary: water damage restoration in Arlington VA (target 1.5-2.0%)
Secondary: Arlington water damage company (target 0.5-1.0%)
Tertiary: water damage repair near Ballston (target 0.3-0.5%)
Geo terms: Arlington, Virginia, Northern Virginia, DMV (natural mentions)
```

## Cannibalization Detection

### What Is Cannibalization?
Two or more pages from the same site competing for the same search query, splitting ranking signals and reducing both pages' performance.

### Detection Process

1. **Collect target keywords** for each URL in inventory
2. **Compare keyword overlap**: Flag pages with >70% keyword overlap
3. **Check GSC data** (if available): Multiple URLs ranking for same query
4. **Evaluate intent**: Do pages serve different user intents?

### Cannibalization Signals

| Signal | Severity | Description |
|--------|----------|-------------|
| Same primary keyword | Critical | Two pages targeting identical primary |
| Same H1 | Critical | Identical or near-identical H1 tags |
| >80% title overlap | High | Titles too similar |
| Same URL ranking for query | High | GSC shows URL switching |
| Same meta description | Medium | Descriptions targeting same keyword |
| >70% content overlap | Critical | Near-duplicate content |

### Resolution Strategies

| Strategy | When to Use |
|----------|------------|
| Consolidate | Merge thin pages into one comprehensive page |
| Differentiate | Rewrite to target distinct keywords/intents |
| Canonical | Point duplicate to primary version |
| Redirect (301) | Remove weaker page, redirect to stronger |
| Noindex | Keep page but remove from index |

## Output Format

```json
{
  "url": "https://example.com/water-damage-arlington-va",
  "primary_keyword": "water damage restoration Arlington VA",
  "analysis": {
    "density": {
      "primary": { "count": 8, "total_words": 650, "density": 1.23, "status": "optimal" },
      "secondary": [
        { "keyword": "water damage company", "count": 3, "density": 0.46, "status": "low" }
      ],
      "total_keyword_footprint": 5.2
    },
    "placement": {
      "title": true,
      "h1": true,
      "first_100_words": true,
      "url": true,
      "meta_description": true,
      "h2_headings": 2,
      "image_alt": false,
      "last_paragraph": true,
      "score": 87
    },
    "issues": [
      { "type": "missing_placement", "detail": "Primary keyword not in any image alt text", "severity": "medium" }
    ],
    "cannibalization": {
      "detected": false,
      "competing_urls": []
    },
    "score": 82
  }
}
```
