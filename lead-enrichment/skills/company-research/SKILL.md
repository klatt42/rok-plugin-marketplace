---
name: company-research
description: |
  Company research and lead enrichment methodology for restoration industry
  prospecting. Tiered research approach covering identity, business intelligence,
  engagement signals, and relationship context. Structured output for company
  profiles including IICRC certifications, carrier relationships, TPA networks,
  Xactimate usage, and competitive positioning. Quality scoring and source
  attribution for all gathered intelligence.
triggers:
  - "research company"
  - "enrich lead"
  - "company lookup"
  - "business intelligence"
  - "company profile"
  - "lead research"
version: 1.0
author: ROK Agency
---

# Company Research Skill

## Research Methodology

Use a four-tier approach to build comprehensive company intelligence. Complete each tier before moving to the next.

### Tier 1: Identity

Establish basic company facts:

| Data Point | Search Strategy |
|-----------|----------------|
| Legal name | `"[company]" site:opencorporates.com OR site:bizapedia.com` |
| DBA / trade names | `"[company]" "doing business as" OR "DBA"` |
| Founded / age | `"[company]" "founded" OR "established" OR "since"` |
| Headquarters | `"[company]" headquarters OR "main office" address` |
| Service area | `"[company]" "service area" OR "we serve" OR territory` |
| Website | Direct search + verify |
| Phone / email | Website contact page, Google Business listing |
| Key principals | `"[company]" "owner" OR "president" OR "CEO" OR "founder"` |

### Tier 2: Business Intelligence

Understand their operations and market position:

| Data Point | Search Strategy |
|-----------|----------------|
| Services offered | Website services page, Google Business categories |
| Certifications | `"[company]" IICRC OR "certified" OR "licensed"` |
| Insurance work | `"[company]" "insurance" OR "claims" OR "carrier" OR "TPA"` |
| Xactimate usage | `"[company]" Xactimate OR "Xactware" OR "estimating"` |
| Carrier relationships | `"[company]" "preferred vendor" OR "network" OR "program"` |
| TPA affiliations | `"[company]" "CRAW" OR "Contractor Connection" OR "HVACi" OR "PSA"` |
| Employee count | LinkedIn company page, website "about" section |
| Revenue signals | Inc 5000, BBB, industry awards |

### Tier 3: Engagement Signals

Find triggers for outreach timing:

| Signal | Search Strategy |
|--------|----------------|
| Recent news | `"[company]" news OR press release (past 3 months)` |
| Job postings | `"[company]" site:indeed.com OR site:linkedin.com/jobs` |
| Awards / recognition | `"[company]" award OR recognition OR "best of"` |
| Social media activity | LinkedIn company page, Facebook, Google reviews |
| Industry events | `"[company]" conference OR trade show OR IICRC OR RIA` |
| Growth signals | New locations, hiring, acquisitions |
| Pain signals | Negative reviews, complaints, BBB issues |

### Tier 4: Relationship Context

Map connections for warm introductions:

| Context | Search Strategy |
|---------|----------------|
| Mutual connections | LinkedIn mutual connections with Prism team |
| Shared carriers | Carriers that both companies work with |
| Industry associations | RIA, IICRC, local restoration associations |
| Complementary services | Services they offer that Prism doesn't (and vice versa) |
| Geographic overlap | Shared service territory |
| Referral potential | Do they handle work types Prism specializes in? |

## Structured Output Format

After research, compile findings into this JSON structure:

```json
{
  "company": {
    "name": "Company Legal Name",
    "dba": "Trade Name (if different)",
    "website": "https://...",
    "phone": "xxx-xxx-xxxx",
    "email": "info@...",
    "address": "123 Main St, City, ST ZIP",
    "founded": "YYYY",
    "employee_count": "estimated range",
    "service_area": "geographic description"
  },
  "principals": [
    {
      "name": "Full Name",
      "title": "Owner / President / etc.",
      "linkedin_url": "",
      "email": "",
      "phone": ""
    }
  ],
  "business_intel": {
    "services": ["list", "of", "services"],
    "certifications": ["IICRC", "specific certs"],
    "insurance_work": "Yes/No/Unclear — details",
    "xactimate": "Yes/No/Unknown",
    "carrier_relationships": ["carrier names if known"],
    "tpa_affiliations": ["TPA names if known"],
    "revenue_signals": "description of size/growth indicators"
  },
  "engagement_signals": {
    "recent_news": ["headline — source — date"],
    "job_postings": ["role — platform — date"],
    "awards": ["award — year"],
    "growth_signals": "description",
    "pain_signals": "description"
  },
  "relationship_context": {
    "mutual_connections": ["name — connection type"],
    "shared_carriers": ["carrier names"],
    "industry_associations": ["association memberships"],
    "complementary_services": "how services complement Prism",
    "referral_potential": "HIGH / MEDIUM / LOW — reasoning"
  },
  "quality_score": {
    "data_completeness": 0,
    "source_count": 0,
    "confidence": "HIGH / MEDIUM / LOW",
    "gaps": ["what couldn't be found"]
  }
}
```

## Restoration Industry Specifics

### Certifications to Look For
- IICRC (Institute of Inspection, Cleaning and Restoration Certification)
  - WRT (Water Restoration Technician)
  - FSRT (Fire and Smoke Restoration Technician)
  - OCT (Odor Control Technician)
  - AMRT (Applied Microbial Remediation Technician)
  - CCT (Commercial Carpet Cleaning Technician)
- RIA (Restoration Industry Association) membership
- State contractor licenses
- EPA Lead-Safe certification
- OSHA certifications

### TPA / Network Programs
- Contractor Connection (Crawford)
- CRAW (Crawford & Company)
- PSA (Paul Davis Systems of America) network
- HVACi (for HVAC-related claims)
- Code Blue
- Signal Restoration
- FirstOnSite network
- DKI (Disaster Kleenup International)

### Key Terminology
- **Xactimate**: Industry-standard estimating software for insurance claims
- **Contents pack-out**: Removing and inventorying personal property from a loss site
- **Mitigation**: Emergency response to stop further damage
- **Reconstruction**: Rebuilding after a loss
- **Subrogation**: Carrier recovering costs from responsible party

## Quality Scoring

| Score | Label | Criteria |
|-------|-------|----------|
| 90-100 | Excellent | All four tiers complete, multiple sources confirm data |
| 70-89 | Good | Tiers 1-3 complete, some Tier 4, minor gaps |
| 50-69 | Fair | Tiers 1-2 complete, limited signals and context |
| 0-49 | Poor | Major gaps in basic identity or business intel |

## Source Attribution

Always record where each data point was found:
- `linkedin` — LinkedIn profile or company page
- `website` — Company's own website
- `google_business` — Google Business Profile / Maps
- `bbb` — Better Business Bureau
- `state_registry` — State corporation/contractor registry
- `news` — News article or press release
- `review_site` — Yelp, Google Reviews, Angi, etc.
- `industry_dir` — Industry directory (RIA, IICRC, etc.)
- `job_board` — Indeed, LinkedIn Jobs, etc.
- `social_media` — Facebook, Instagram, etc.
