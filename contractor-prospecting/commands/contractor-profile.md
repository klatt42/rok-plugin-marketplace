# Contractor Profile

You are building a comprehensive profile on a specific contractor or contracting company for Prism Specialties DMV's referral development efforts.

## Input

The user will provide:
- **Company name** (required)
- **Key contact name** (helpful if provided)
- **Location** (helpful if provided)

## Process

### Step 1: Research the Contractor

Run multiple targeted searches:

1. **Company website**: `"[company name]" restoration OR contractor [location]`
2. **LinkedIn company page**: `"[company name]" site:linkedin.com`
3. **LinkedIn key people**: `"[company name]" ("owner" OR "president" OR "operations") site:linkedin.com`
4. **Google reviews**: Search Google Maps for the company
5. **License verification**: Check VA DPOR, MD MHIC, or DC DCRA depending on location
6. **Industry directories**: Search RIA, IICRC, BBB for the company
7. **Carrier vendor programs**: `"[company name]" "preferred vendor" OR "select service" OR "approved contractor"`
8. **News/community**: `"[company name]" [location] restoration OR contractor`

### Step 2: Build Profile

Compile everything found into a structured profile:

```
## Contractor Profile: [Company Name]

### Quick Take
[2-3 sentence summary: who they are, what they do, why they matter to Prism as a referral partner]

### Company Details
| Field | Details |
|-------|---------|
| Company Name | |
| Type | [Restoration / GC / Mitigation / Franchise] |
| Franchise Brand | [If applicable] |
| Key Contact | [Name, Title] |
| Owner/Principal | |
| Years in Business | |
| Employees (est.) | |
| Website | |
| LinkedIn | [Company page URL] |
| Phone | |
| Address | |

### Licensing & Credentials
| State | License # | Type | Status |
|-------|----------|------|--------|
| VA | | DPOR Class [A/B/C] | |
| MD | | MHIC # | |
| DC | | DCRA | |

**Certifications**: [IICRC, RIA member, BBB accredited, etc.]

### Service Area & Territory
- Primary area: [specific counties/cities]
- Territory overlap with Prism: [HIGH/MEDIUM/LOW]
- Office locations: [addresses if found]

### Services Offered
- [List services — look for what they DON'T do (contents, electronics, documents)]
- **Contents capability**: [None / Basic / Advanced]
- **Gap Prism fills**: [Specific services Prism would provide that they don't]

### Insurance Work Focus
- Carrier relationships: [Any carriers mentioned on website or reviews]
- Preferred vendor programs: [Any carrier vendor programs they're part of]
- Insurance work percentage: [estimate based on reviews/website]
- TPA relationships: [Any third-party administrator connections]

### Volume & Reputation
- Google rating: [X.X stars, Y reviews]
- Yelp rating: [if available]
- Angi/HomeAdvisor: [if available]
- BBB rating: [if available]
- Estimated monthly insurance jobs: [based on review volume and territory]

### Key People to Contact
| Name | Title | LinkedIn | Notes |
|------|-------|----------|-------|
| | | | |

### Referral Relationship Entry Points
- Mutual connections: [any shared LinkedIn connections, industry contacts]
- Shared carrier relationships: [both work with same carriers?]
- Industry events: [RIA, IICRC, ABC membership overlap]
- Shared territory: [specific areas where both operate]
- Recent jobs: [any recent losses where both could have been involved]

### Talking Points for Outreach
1. [Specific hook based on their services or territory]
2. [Reference to a gap Prism can fill]
3. [Mutual benefit angle]

### Referral Potential Score
[HIGH / MEDIUM / LOW] — [brief rationale]
- Territory overlap: [HIGH/MEDIUM/LOW]
- Insurance focus: [HIGH/MEDIUM/LOW]
- Contents gap (needs Prism): [HIGH/MEDIUM/LOW]
- Volume: [HIGH/MEDIUM/LOW]
- Accessibility: [HIGH/MEDIUM/LOW]
```

### Step 3: Suggest Next Actions

- If HIGH referral potential: "Ready for outreach — run `/contractor-prospecting:contractor-outreach [company name]`"
- If MEDIUM: "Consider researching [specific gap] or connecting at [upcoming event]"
- If LOW: "This contractor may not be the best referral target. Reason: [specifics]"

## Rules

- Only use publicly available information — never fabricate details
- If you can't find specific information, say "Not found" rather than guessing
- Be honest about confidence level — "Website states..." vs "Based on reviews, likely..."
- The Referral Potential Score should be realistic, not optimistic
- Pay special attention to whether they have in-house contents restoration (if yes, referral potential drops)
- Franchise owners are often the best entry point — they're local decision makers
- Always suggest concrete next steps
