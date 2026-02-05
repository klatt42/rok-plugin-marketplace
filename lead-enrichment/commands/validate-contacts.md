# Validate Contacts

You are executing a batch contact validation workflow. Your goal is to validate email addresses and phone numbers for a list of contacts, scoring each for reliability.

## Input

The user will provide contacts in one of these formats:
- **File path**: CSV, JSON, or text file with contact data
- **Pasted list**: Names, emails, phones pasted directly in chat
- **Session data**: "Validate the contacts from the last enrichment"

If no input is provided, ask the user how they'd like to provide the contact list.

## Process

### Step 1: Parse Input

Extract contacts into a structured list:

| # | Name | Title | Company | Email | Phone |
|---|------|-------|---------|-------|-------|
| 1 | ... | ... | ... | ... | ... |

Present the parsed list: "I found [X] contacts to validate. Proceeding with Level 1-2 validation."

### Step 2: Level 1 — Syntax Validation (Automatic)

For each contact, check:

**Emails**:
- Valid format (local@domain.tld)
- No invalid characters or patterns
- TLD exists
- Not a known disposable domain (check against the disposable domains list in contact-validation skill)

**Phones**:
- Contains 10+ digits
- Valid area code (not 555, 000, etc.)
- Not a sequential or all-same-digit pattern

Mark each as `syntax_valid` or `syntax_invalid` with reason.

### Step 3: Level 2 — Domain/Format Verification (Automatic)

For each email that passed Level 1:

```bash
# Check MX records for each unique domain
dig +short MX [domain.com]
```

- MX records found → `domain_valid`
- Domain resolves, no MX → `domain_partial`
- Domain doesn't resolve → `domain_invalid`

For phones:
- Identify type (landline, mobile, toll-free, VoIP) by area code
- Flag any premium rate numbers

### Step 4: Present Results

Display the validation report:

```
## Contact Validation Report

### Summary
- Total Contacts: [X]
- Valid: [X] (score >= 70)
- Uncertain: [X] (score 50-69)
- Invalid: [X] (score < 50)
- Average Score: [X]/100

### Detailed Results

| # | Name | Email | Email Status | Phone | Phone Status | Score | Flags |
|---|------|-------|-------------|-------|-------------|-------|-------|
| 1 | ... | ... | valid | ... | valid | 92 | — |
| 2 | ... | ... | domain_invalid | ... | syntax_valid | 35 | bad domain |

### Red Flags
- [Contact Name]: [specific issue]
```

### Step 5: APPROVAL GATE for Level 3

If the user wants external API verification:

"Level 3 verification uses external APIs to check if mailboxes exist and if phone numbers are active. This requires API access. Do you have API keys configured for any of these services?"
- Hunter.io
- NeverBounce
- ZeroBounce
- NumVerify
- Twilio Lookup

**Wait for explicit user approval and API details before proceeding with Level 3.**

### Step 6: Export

Offer to export the validation results:

"Would you like to export this validation report to Excel?"

If yes, construct the JSON payload:

```json
{
  "type": "leads",
  "carrier": "[Company Name or 'Batch Validation']",
  "region": "DMV",
  "date": "YYYY-MM-DD",
  "report_type": "Validation",
  "search_summary": "Contact validation for [X] contacts",
  "records": [
    {
      "name": "Contact Name",
      "title": "Title",
      "company": "Company Name",
      "email": "email@domain.com",
      "phone": "(xxx) xxx-xxxx",
      "validation_status": "valid",
      "confidence": 92,
      "priority": "high",
      "category": "decision_maker",
      "industry": "",
      "notes": "L1: syntax_valid, L2: domain_valid, MX: 3 records"
    }
  ],
  "analysis": "Validation summary text",
  "next_steps": ["Follow up with valid contacts", "Re-verify uncertain contacts manually"]
}
```

Write to temp file and run:
```bash
cat > /tmp/validation_export.json << 'EXPORT_EOF'
{ ... json payload ... }
EXPORT_EOF

~/.claude/scripts/.venv/bin/python3 ~/.claude/scripts/prospecting_export.py \
  --input /tmp/validation_export.json

rm /tmp/validation_export.json
```

Report output file paths.

## Rules

- Level 1 and Level 2 validation run automatically — no user approval needed
- Level 3 (external API) always requires explicit user approval
- Never send contact data to external services without user consent
- Report all red flags clearly — don't hide bad data
- If a file path is provided, verify it exists before attempting to read
- Score every contact consistently using the quality scoring from the contact-validation skill
