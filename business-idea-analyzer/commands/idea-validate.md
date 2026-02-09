# Idea Validate

Build an assumption inventory for a business opportunity with verification methods, pass/fail criteria, and kill conditions. This command turns vague confidence into a testable checklist -- every assumption gets a specific, quantified threshold for validation.

## Usage

```
/business-idea-analyzer:idea-validate AI inventory management tool for eBay sellers
/business-idea-analyzer:idea-validate Chrome extension for Etsy analytics --strictness=strict
/business-idea-analyzer:idea-validate --source="Seller Analytics Dashboard" --strictness=lenient
```

### Arguments

- **idea description** (required unless `--source` provided): The business opportunity to validate.
- **--source** (optional): Name of an opportunity from a previous `/analyze-idea` or `/idea-deep-dive` session.
- **--strictness** (optional): `lenient`, `standard` (default), or `strict`. Controls how aggressively assumptions are flagged as critical.

Initial request: $ARGUMENTS

## Strictness Levels

| Level | Critical Flags | Use When |
|-------|---------------|----------|
| **lenient** | Only truly fatal kills: platform shutdown, legal prohibition, technical impossibility | Early brainstorming, exploring many ideas |
| **standard** | Critical + high-impact kills: market too small, no willingness to pay, strong incumbents | Default for most analyses |
| **strict** | All severity levels flagged: includes moderate risks like slow adoption, feature parity | Pre-investment, committing significant resources |

## Process

### Step 1: Establish Context

**If `--source` provided:**
- Look for the named opportunity in the current session context.
- Extract existing findings, scores, and risk signals as a starting point.
- If not found, ask the user to provide the idea description or run an analysis first.

**If new idea description provided:**
- Run 3-5 WebSearch queries to understand the assumption landscape:
  - `"[idea keywords]" market size OR total addressable market`
  - `"[idea keywords]" willingness to pay OR pricing survey`
  - `"[idea keywords]" technical feasibility OR API OR platform rules`
  - `"[idea keywords]" regulation OR legal OR compliance`
  - `"[idea keywords]" competitor OR incumbent OR market leader`

### Step 2: Generate Assumption Inventory

Identify 10-20 assumptions across 5 categories. Each assumption must be specific and testable -- not vague.

**Bad assumption:** "People want this product"
**Good assumption:** "eBay sellers with 100+ monthly listings will pay $29/mo for automated inventory sync"

#### Categories

**Market Assumptions (3-5):**
- Target user exists in sufficient numbers
- Pain point is severe enough to drive purchase
- Market is growing or stable (not shrinking)
- Users actively seek solutions (demand signals)

**Technical Assumptions (2-4):**
- Required APIs/platforms are accessible and stable
- Core feature is technically buildable by a solo dev in [X] weeks
- No platform ToS violations
- Data sources are reliable and legal to access

**Financial Assumptions (2-4):**
- Users will pay [specific price] for [specific value]
- Unit economics work at projected scale
- Customer acquisition cost is sustainable
- Revenue covers infrastructure costs by month [X]

**Competitive Assumptions (2-3):**
- Identified gap is not already being filled
- Incumbents cannot easily replicate the differentiator
- Switching costs for users are low enough to acquire them

**Regulatory Assumptions (1-3):**
- No legal barriers to operating in target markets
- Data handling complies with relevant regulations
- Platform terms of service permit the proposed use case

### Step 3: Define Verification Framework

For each assumption, determine:

| Field | Description |
|-------|-------------|
| **ID** | ASM-001, ASM-002, etc. |
| **Category** | Market / Technical / Financial / Competitive / Regulatory |
| **Assumption** | Specific, testable statement |
| **Confidence** | LOW / MEDIUM / HIGH (based on current evidence) |
| **Verification Method** | How to test: survey, landing page, API test, competitor analysis, legal review |
| **Pass Criteria** | Quantified threshold: ">=200 responses indicate willingness to pay $29/mo" |
| **Fail Criteria** | Quantified threshold: "<50 responses or <30% willing to pay any price" |
| **Kill Condition** | What would make the entire idea unviable if this assumption fails |
| **Priority** | Must verify before MVP / Should verify before launch / Can verify after launch |

### Step 4: Apply Strictness Filter

Based on the `--strictness` flag, determine which assumptions are flagged as CRITICAL:

**Lenient:** Only flag assumptions where the kill condition involves:
- Platform/API shutdown or access revocation
- Legal prohibition or regulatory block
- Technical impossibility (not just difficulty)

**Standard:** Flag the above plus:
- TAM below viable threshold
- No evidence of willingness to pay
- Strong incumbent with >70% market share and high switching costs
- Unit economics negative at projected scale

**Strict:** Flag all of the above plus:
- Slow adoption risk (time to 100 users > 6 months)
- Feature parity risk (competitors can copy within 3 months)
- Single-channel dependency (>80% of acquisition from one source)
- Founder-market fit concerns

### Step 5: Prioritize and Present

Group assumptions into three priority tiers and present as a checklist:

```markdown
## Assumption Validation Checklist: [Idea Name]

**Date:** [YYYY-MM-DD] | **Strictness:** [lenient/standard/strict]
**Total Assumptions:** [N] | **Critical Kills:** [N] | **Overall Risk Level:** [LOW/MEDIUM/HIGH]

---

### MUST Verify Before MVP

These assumptions are foundational. If any fail, reconsider the idea.

- [ ] **ASM-001** [CRITICAL] [Market]
  **Assumption:** [Specific statement]
  **Confidence:** LOW
  **Verify by:** [Method -- e.g., "Run a 50-person survey on r/eBaySellers"]
  **Pass:** [Quantified -- e.g., ">=60% indicate they would pay $20+/mo"]
  **Fail:** [Quantified -- e.g., "<30% interested at any price point"]
  **Kill if:** [Condition -- e.g., "No measurable demand signal after 2 weeks of outreach"]

- [ ] **ASM-002** [CRITICAL] [Technical]
  **Assumption:** [Statement]
  **Confidence:** MEDIUM
  **Verify by:** [Method]
  **Pass:** [Threshold]
  **Fail:** [Threshold]
  **Kill if:** [Condition]

---

### SHOULD Verify Before Launch

Important for business viability but not immediate blockers.

- [ ] **ASM-005** [Financial]
  **Assumption:** [Statement]
  **Confidence:** MEDIUM
  **Verify by:** [Method]
  **Pass:** [Threshold]
  **Fail:** [Threshold]

---

### CAN Verify After Launch

Lower-risk assumptions that real usage data will validate.

- [ ] **ASM-010** [Competitive]
  **Assumption:** [Statement]
  **Confidence:** HIGH
  **Verify by:** [Method]
  **Pass:** [Threshold]
  **Fail:** [Threshold]

---

### Summary

| Category | Total | Critical | Avg Confidence |
|----------|-------|----------|---------------|
| Market | X | X | LOW/MED/HIGH |
| Technical | X | X | LOW/MED/HIGH |
| Financial | X | X | LOW/MED/HIGH |
| Competitive | X | X | LOW/MED/HIGH |
| Regulatory | X | X | LOW/MED/HIGH |

### Verdict

[1-3 sentences: Overall validation risk assessment. How many critical kills exist, what is the biggest unknown, and what single action would most reduce uncertainty.]

### Next Steps
- Run the top 3 verification methods before committing to build
- Deep dive on the idea: `/business-idea-analyzer:idea-deep-dive [idea]`
- Full scored analysis: `/business-idea-analyzer:analyze-idea [idea]`
- Export results: `/business-idea-analyzer:idea-export`
```

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- Every assumption must be specific and testable. Reject vague assumptions like "the market exists."
- Pass and fail criteria must include numbers or quantified thresholds -- not subjective judgments.
- Kill conditions must describe a concrete, observable outcome, not a feeling.
- Do not fabricate verification results. This command defines WHAT to test, not the test outcomes.
- All evidence and context must come from WebSearch. Cite sources when establishing confidence levels.
- Do not launch subagents. All research runs in the main thread.
- Output stays in chat. The user can run `/idea-export` separately to generate files.
