---
name: legal-analysis
description: |
  Legal case building patterns for commercial landlord-tenant disputes.
  Claim type definitions, evidence strength assessment, Maryland-specific
  commercial tenant remedies, argument structure templates, and damage
  calculation frameworks. Used when constructing legal arguments,
  evaluating evidence, or preparing attorney deliverables.
triggers:
  - "legal claim"
  - "evidence"
  - "breach of contract"
  - "negligence"
  - "case building"
  - "constructive eviction"
  - "OPEX fraud"
  - "legal argument"
  - "attorney brief"
  - "claim strength"
version: 1.0
author: ROK Agency
---

# Legal Analysis Skill

## Claim Types and Elements

### Breach of Contract
**Elements to prove:**
1. Valid lease agreement exists
2. Specific lease provision was violated
3. Landlord was notified of the breach
4. Landlord failed to cure within reasonable time
5. Tenant suffered damages

**Evidence needed:** Signed lease, breach notifications (emails), cure period documentation, damage calculations

**Strength assessment:**
- STRONG: Clear lease provision + documented breach + written notice + no cure
- MODERATE: Clear provision + breach pattern + verbal or indirect notice
- SUPPORTING: Implied obligation + circumstantial evidence of breach

### Gross Negligence
**Elements to prove:**
1. Duty of care existed (lease/statute)
2. Conduct was far below reasonable standard
3. Defendant knew or should have known of the risk
4. Conduct caused the harm

**Evidence needed:** Industry standards, inspection reports, known defect documentation, failure pattern analysis

**Key distinction:** Gross negligence requires showing conduct "far below" reasonable care — not just ordinary negligence. Pattern of repeated failures strengthens this.

### Constructive Eviction
**Elements to prove (Maryland):**
1. Landlord's action or failure to act
2. Made premises substantially unsuitable for intended purpose
3. Tenant gave notice of condition
4. Tenant vacated within reasonable time (OR in MD: may be able to claim without vacating for commercial)

**Evidence needed:** Temperature logs, habitability complaints, business impact documentation, notification chain

### OPEX Fraud / Misallocation
**Elements to prove:**
1. Lease defines OPEX calculation methodology
2. Landlord deviated from lease methodology
3. Deviation was intentional or reckless
4. Tenant was overcharged

**Evidence needed:** OPEX statements, lease calculation provisions, audit requests and responses, comparable building data

### Failure to Repair
**Elements to prove (Maryland Commercial):**
1. Repair obligation exists (lease or implied warranty)
2. Landlord was notified of need for repair
3. Reasonable time to repair elapsed
4. Repair was not made or was inadequate

**Evidence needed:** Repair requests (dated), response timeline, work orders, follow-up complaints

## Evidence Strength Assessment

| Strength | Criteria | Use |
|----------|----------|-----|
| **STRONG** | Direct evidence, documented, corroborated by multiple sources | Lead evidence in argument |
| **MODERATE** | Clear evidence but limited corroboration or slight ambiguity | Supporting evidence |
| **SUPPORTING** | Circumstantial, pattern-based, or inferential | Background context |
| **WEAK** | Single source, uncorroborated, or subject to interpretation | Mention only if nothing stronger exists |

## Confidence Formula

```
evidence_confidence = (
    source_reliability * 0.3 +
    corroboration_score * 0.3 +
    directness * 0.2 +
    documentation_quality * 0.2
)
```

Where:
- `source_reliability`: Official document (1.0), email (0.8), verbal/noted (0.4)
- `corroboration_score`: Multiple independent sources (1.0), single strong (0.7), uncorroborated (0.3)
- `directness`: Direct evidence of claim element (1.0), circumstantial (0.5), inferential (0.3)
- `documentation_quality`: Dated + signed (1.0), dated (0.8), undated (0.4)

## Maryland Commercial Tenant Remedies

**Md. Code, Real Prop. § 8-211.1** (Commercial properties):
- Tenant may repair and deduct if landlord fails to maintain after notice
- Self-help remedies available for essential services
- Rent abatement for substantial interference with use

**Common Law Remedies:**
- Breach of contract damages
- Constructive eviction (with or without vacating in some jurisdictions)
- Rent withholding (with proper notice)
- Lease termination for material breach

## Damage Calculation Framework

| Category | Calculation Method |
|----------|-------------------|
| Direct repair costs | Actual invoices + vendor quotes |
| Business interruption | Revenue loss during unusable periods |
| Rent abatement | Pro-rata reduction for unusable space |
| OPEX overcharges | Difference between charged and correct amounts |
| Supplemental equipment | Cost of temporary heating/cooling |
| Attorney fees | If lease provides for fee-shifting |
| Consequential damages | Provable downstream business losses |

## Argument Structure Template

```markdown
## [Claim Type]: [One-line summary]

### Legal Standard
[Cite applicable law and lease provisions]

### Facts
[Chronological narrative of relevant facts, citing Doc #IDs]

### Evidence Chain
1. [Date] - [Event] (Doc #ID)
2. [Date] - [Event] (Doc #ID)
...

### Analysis
[How the facts meet each element of the claim]

### Damages
[Calculation of damages attributable to this claim]

### Strength Assessment
Overall: [STRONG/MODERATE/SUPPORTING]
Key strengths: [list]
Key weaknesses: [list]
```
