---
name: contact-validation
description: |
  Contact validation methodology for email addresses and phone numbers.
  Multi-level validation from syntax checking through domain verification
  to external API verification. Red flags detection for disposable domains,
  fake patterns, and spam traps. Quality scoring and structured output for
  validated contact data. Used during lead enrichment workflows.
triggers:
  - "validate email"
  - "validate phone"
  - "contact validation"
  - "verify contacts"
  - "check email"
  - "verify email"
version: 1.0
author: ROK Agency
---

# Contact Validation Skill

## Validation Levels

### Level 1: Syntax Validation (Automatic)

No external calls required. Run immediately on all contacts.

**Email checks**:
- Valid format: `local@domain.tld`
- No spaces, double dots, or invalid characters
- TLD exists and is reasonable length
- Local part not excessively long (>64 chars)

**Phone checks**:
- Contains 10+ digits (US format)
- Valid area code (not 555, 000, etc.)
- Matches common formats: (xxx) xxx-xxxx, xxx-xxx-xxxx, +1xxxxxxxxxx

**Result**: `syntax_valid` or `syntax_invalid` with specific error

### Level 2: Domain/Format Verification (Automatic)

Uses built-in tools, no external APIs.

**Email domain verification** (using `dig` command):
```bash
# Check if domain has MX records
dig +short MX example.com

# Check if domain resolves at all
dig +short A example.com
```

- Domain has MX records → `domain_valid`
- Domain resolves but no MX → `domain_partial` (may still work)
- Domain doesn't resolve → `domain_invalid`

**Phone type detection**:
- Area code lookup for geographic region
- Identify toll-free (800, 888, 877, 866, 855, 844, 833)
- Identify known VoIP ranges

**Result**: `domain_valid`, `domain_partial`, or `domain_invalid`

### Level 3: External Verification (Requires Approval)

Uses external APIs — always ask user before proceeding.

**Email verification APIs** (if user has access):
- Hunter.io email verification
- NeverBounce
- ZeroBounce
- Abstract API Email Validation

**Phone verification APIs** (if user has access):
- NumVerify
- Twilio Lookup
- Abstract API Phone Validation

**Result**: `verified`, `unverified`, `catch_all`, `disposable`, `invalid`

## Red Flags

### Email Red Flags

| Pattern | Risk | Action |
|---------|------|--------|
| Disposable domain (mailinator, guerrillamail, tempmail, etc.) | High | Flag as `disposable` |
| Random character string local part | Medium | Flag as `suspicious` |
| Generic role address (info@, admin@, sales@) | Low | Note as `role_address` |
| Newly registered domain (<30 days) | Medium | Flag as `new_domain` |
| Known spam trap patterns | High | Flag as `spam_trap` |
| Free email for business contact (gmail for "VP" title) | Low | Note as `personal_email` |

### Common Disposable Email Domains

```
mailinator.com, guerrillamail.com, tempmail.com, throwaway.email,
yopmail.com, 10minutemail.com, trashmail.com, sharklasers.com,
guerrillamailblock.com, grr.la, discard.email, mailnesia.com,
maildrop.cc, fakeinbox.com, temp-mail.org
```

### Phone Red Flags

| Pattern | Risk | Action |
|---------|------|--------|
| 555-xxxx numbers | High | Flag as `fake` |
| All same digit (000-000-0000) | High | Flag as `fake` |
| Sequential (123-456-7890) | High | Flag as `fake` |
| Premium rate (900, 976) | Medium | Flag as `premium` |
| International format for US company | Low | Note as `international` |

## Quality Scoring

### Per-Contact Score

| Score | Label | Criteria |
|-------|-------|----------|
| 90-100 | Excellent | L1 + L2 pass, no red flags, matches company domain |
| 70-89 | Good | L1 + L2 pass, minor flags (personal email, etc.) |
| 50-69 | Fair | L1 pass, L2 partial or untested |
| 0-49 | Poor | L1 fail, red flags present, or invalid domain |

### Batch Score

Average of individual scores, weighted by contact priority.

## Validation Output Format

```json
{
  "validation_summary": {
    "total_contacts": 0,
    "validated": 0,
    "valid": 0,
    "invalid": 0,
    "uncertain": 0,
    "average_score": 0,
    "validation_date": "YYYY-MM-DD"
  },
  "contacts": [
    {
      "name": "Contact Name",
      "title": "Title",
      "company": "Company Name",
      "email": {
        "address": "user@example.com",
        "level_1": "syntax_valid",
        "level_2": "domain_valid",
        "level_3": "not_checked",
        "red_flags": [],
        "score": 85,
        "status": "valid"
      },
      "phone": {
        "number": "(xxx) xxx-xxxx",
        "level_1": "syntax_valid",
        "level_2": "format_valid",
        "level_3": "not_checked",
        "type": "landline",
        "red_flags": [],
        "score": 80,
        "status": "valid"
      },
      "overall_score": 83,
      "overall_status": "valid"
    }
  ]
}
```

## Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| `valid` | Passed all checked levels, no red flags | Safe to use |
| `likely_valid` | Passed L1-L2, minor flags | Use with caution |
| `uncertain` | Partial results, couldn't fully verify | Verify manually |
| `invalid` | Failed validation or major red flags | Do not use |
| `not_checked` | Level not yet run | Run validation |

## Integration with Lead Enrichment

When called from `/enrich-lead`:
1. Receive contacts from company research phase
2. Run Level 1 + Level 2 automatically
3. Present results with scores to user
4. If user approves, offer Level 3 (external API) validation
5. Return validated contacts for export

When called from `/validate-contacts`:
1. Accept batch input (file, pasted list, or session data)
2. Parse contacts into structured format
3. Run Level 1 + Level 2 automatically
4. Report per-contact and batch scores
5. Offer Level 3 if user has API access
6. Export results to Excel with conditional formatting
