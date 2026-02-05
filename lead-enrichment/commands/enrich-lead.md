# Enrich Lead

You are executing a lead enrichment workflow for Prism Specialties DMV. Your goal is to research a company, discover key contacts, validate their information, and produce a comprehensive enrichment report.

## Input

The user will provide:
- **Company name** (required) — if not provided, ask for it
- **Industry focus** (optional) — default: restoration / insurance / construction
- **Geographic focus** (optional) — default: DMV area

## Process

### Step 1: Company Research

Use the company-research skill methodology to build a complete company profile.

**Execute web searches in this order**:

1. `"[company name]" site:linkedin.com/company` — LinkedIn company page
2. `"[company name]" restoration OR contractor OR construction [location]` — general presence
3. `"[company name]" IICRC OR "certified" OR "licensed" OR "insured"` — certifications
4. `"[company name]" "preferred vendor" OR "insurance" OR "carrier" OR "claims"` — insurance relationships
5. `"[company name]" Xactimate OR "estimating" OR "TPA"` — industry tools
6. `"[company name]" news OR "press release" (recent)` — engagement signals
7. `"[company name]" site:indeed.com OR site:glassdoor.com` — hiring signals
8. `"[company name]" reviews OR "BBB" OR site:yelp.com` — reputation

Compile findings into the structured company profile format from the company-research skill.

### Step 2: Contact Discovery

Search for decision makers and key contacts:

1. `"[company name]" "owner" OR "president" OR "CEO" OR "general manager" site:linkedin.com`
2. `"[company name]" "operations manager" OR "project manager" OR "estimator" site:linkedin.com`
3. `"[company name]" "business development" OR "sales" site:linkedin.com`
4. Website team/about page for listed contacts
5. Google Business Profile for phone/email

For each contact found, record:
- Full name
- Title / role
- Email (if publicly available)
- Phone (if publicly available)
- LinkedIn URL
- Source where found
- Category: `decision_maker`, `department_head`, `key_contact`, or `other`

### Step 3: APPROVAL GATE

**STOP and present findings to the user before proceeding.**

Display:
1. Company overview summary (name, services, service area, size)
2. Contacts found (table: Name | Title | Category | Email | Phone | Source)
3. Quality score so far

Ask: "I found [X] contacts at [company]. Should I proceed with contact validation? (Level 1-2 syntax and domain checks are automatic. Level 3 external API verification would require your approval.)"

**Wait for user confirmation before continuing.**

### Step 4: Contact Validation

After user approval, run validation using the contact-validation skill:

**Level 1 (automatic)**: Syntax check all emails and phone numbers
**Level 2 (automatic)**: Domain/MX verification for emails, format validation for phones

```bash
# For each email domain, verify MX records
dig +short MX [domain.com]
```

Present validation results:
```
| Contact | Email Status | Phone Status | Score |
|---------|-------------|-------------|-------|
| ...     | valid       | valid       | 92    |
```

If any contacts have scores below 50, flag them.

**Level 3**: Only if user explicitly approves and has API keys configured.

### Step 5: Generate Structured Output

Compile all findings into a comprehensive output:

```
## Lead Enrichment Report: [Company Name]

### Company Overview
- Name: [legal name]
- Website: [url]
- Service Area: [geographic description]
- Founded: [year]
- Size: [employee estimate]
- Key Services: [list]

### Key Contacts
| # | Name | Title | Email | Phone | Status | Confidence | Category |
|---|------|-------|-------|-------|--------|-----------|----------|
| 1 | ... | ... | ... | ... | valid | 92 | Decision Maker |

### Business Intelligence
- Insurance Work: [yes/no/details]
- Certifications: [list]
- Carrier Relationships: [known carriers]
- Xactimate: [yes/no]

### Engagement Signals
- [Recent news, job postings, awards, growth indicators]

### Recommended Approach
- [Talking points tailored to this company]
- [Best contact to reach first]
- [Timing considerations]

### Quality Score: [X]/100
- Data Completeness: [X]%
- Sources Used: [X]
- Confidence: HIGH/MEDIUM/LOW
```

### Step 6: Export

After presenting the report, offer export options:

"Would you like to export this enrichment report?"
- **Chat only** — already displayed above
- **PDF** — professional PDF report
- **Excel** — spreadsheet with contacts and company data
- **All** — both PDF and Excel

If the user chooses to export, construct the JSON payload:

```json
{
  "type": "leads",
  "carrier": "[Company Name]",
  "region": "[Service Area or DMV]",
  "date": "YYYY-MM-DD",
  "report_type": "Enrichment",
  "search_summary": "Lead enrichment for [Company Name] — [brief description]",
  "company_overview": {
    "name": "[company name]",
    "website": "[url]",
    "service_area": "[area]",
    "founded": "[year]",
    "employee_count": "[estimate]",
    "services": ["list"],
    "certifications": ["list"],
    "insurance_work": "[details]",
    "xactimate": "[yes/no]",
    "carrier_relationships": ["list"],
    "tpa_affiliations": ["list"]
  },
  "records": [
    {
      "name": "Contact Name",
      "title": "Title",
      "company": "[Company Name]",
      "email": "email@domain.com",
      "phone": "(xxx) xxx-xxxx",
      "validation_status": "valid",
      "confidence": 92,
      "priority": "high",
      "category": "decision_maker",
      "industry": "restoration",
      "notes": "Owner, found via LinkedIn and company website"
    }
  ],
  "signals": [
    {"type": "news", "detail": "headline", "date": "YYYY-MM-DD", "source": "url"},
    {"type": "job_posting", "detail": "role", "date": "YYYY-MM-DD", "source": "url"}
  ],
  "analysis": "Recommended approach and analysis text",
  "next_steps": ["Step 1", "Step 2", "Step 3"]
}
```

Write to temp file and run export:
```bash
cat > /tmp/lead_enrichment_export.json << 'EXPORT_EOF'
{ ... json payload ... }
EXPORT_EOF

~/.claude/scripts/.venv/bin/python3 ~/.claude/scripts/prospecting_export.py \
  --input /tmp/lead_enrichment_export.json

rm /tmp/lead_enrichment_export.json
```

Report output paths to user.

## Rules

- Only use publicly available information
- Never fabricate contacts or data — only report what you actually find
- Always present the APPROVAL GATE before validation
- Level 3 validation requires explicit user approval
- Record the source for every data point
- If searches return no results, say so and suggest alternatives
- Prioritize decision makers (owners, GMs, VPs) over other contacts
- Flag any red flags in contact data (disposable emails, fake phones)
