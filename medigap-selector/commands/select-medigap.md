# Medigap Plan Selector

Interview-driven Medigap Plan G vs Plan N selection for Maryland and Pennsylvania. Gathers your requirements through structured questions, then dispatches 3 parallel research agents to analyze premiums, state regulations, and cost patterns. Produces a scored recommendation with premium tables, break-even analysis, scenario comparisons, and strategic switching advice.

## Usage

```
/medigap-selector:select-medigap                              # Full interview
/medigap-selector:select-medigap --zip=21401                   # Pre-fill MD location
/medigap-selector:select-medigap --zip=15401                   # Pre-fill PA location
/medigap-selector:select-medigap --zip=21401 --age=65          # Pre-fill location + age
```

## Arguments

- **--zip** (optional): Zip code (21401 for MD, 15401 for PA). Skips location question.
- **--age** (optional): Age at enrollment. Skips age question.

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Interview

Conduct a structured interview using `AskUserQuestion` to gather the user's Medigap requirements. Present questions in 2 rounds (plus a conditional round 2.5).

**Parse $ARGUMENTS first**: If `--zip` is provided, determine state from zip (21401 = MD, 15401 = PA) and skip the location question. If `--age` is provided, skip the age portion of Round 1.

**Round 1** — Two questions in a single `AskUserQuestion` call:

**Question 1: Location**
(Skip if --zip provided)
```
header: "Location"
question: "Which area are you in? This determines available insurers and state rules."
multiSelect: false
options:
  - label: "Maryland (21401 - Annapolis area)"
    description: "Has birthday rule — can switch plans annually without underwriting"
  - label: "Pennsylvania (15401 - Uniontown area)"
    description: "No birthday rule — initial plan choice is effectively permanent"
```

**Question 2: Age & Enrollment Status**
(Skip age portion if --age provided)
```
header: "Enrollment"
question: "What is your age and Medicare enrollment status?"
multiSelect: false
options:
  - label: "65 — Initial open enrollment"
    description: "Turning 65 soon or within 6-month open enrollment window"
  - label: "65 — Already enrolled in Medigap"
    description: "Currently have a Medigap plan, considering switching"
  - label: "66-70 — Considering switch"
    description: "Past initial enrollment, exploring options"
  - label: "70+ — Considering switch"
    description: "Well past initial enrollment, want to evaluate current plan"
```

**Round 2** — Two questions in a single `AskUserQuestion` call:

**Question 3: Medical Usage**
```
header: "Usage"
question: "How would you describe your typical annual medical usage?"
multiSelect: false
options:
  - label: "Light (2-4 visits/year)"
    description: "Annual wellness + 1-3 doctor visits, rarely see specialists"
  - label: "Moderate (6-10 visits/year)"
    description: "Regular check-ups, occasional specialist visits, some prescriptions"
  - label: "Heavy (12+ visits/year)"
    description: "Frequent visits, multiple specialists, ongoing conditions"
  - label: "Uncertain"
    description: "New to Medicare, not sure what to expect"
```

**Question 4: Priorities**
```
header: "Priorities"
question: "Which priorities matter most to you? Select all that apply."
multiSelect: true
options:
  - label: "Peace of mind / predictable costs"
    description: "Want to know exactly what you'll pay, no surprises"
  - label: "Lowest monthly premium"
    description: "Minimize the monthly check you write"
  - label: "Best coverage for specialists"
    description: "See specialists frequently, want maximum protection"
  - label: "Flexibility to change later"
    description: "Want options, not locked into one plan forever"
```

**Round 2.5 (Conditional)** — If medical usage is "Moderate" or "Heavy" OR if "Best coverage for specialists" was selected, present this question:

**Question 5: Provider Assignment**
```
header: "Providers"
question: "Do your current doctors accept Medicare assignment (accept Medicare's approved amount as full payment)?"
multiSelect: false
options:
  - label: "Yes, all accept assignment"
    description: "All my providers are participating Medicare providers"
  - label: "Most do, unsure about some specialists"
    description: "Primary care accepts, but not sure about all specialists"
  - label: "Some don't accept assignment"
    description: "I know at least one provider charges more than Medicare approves"
  - label: "I don't know"
    description: "Haven't checked — I can look into this"
```

If usage is "Light" and "Best coverage for specialists" was NOT selected, skip this question and assume "most accept."

After all rounds, build a **Requirements Profile** JSON:
```json
{
  "zip_code": "[from Q1 or --zip]",
  "state": "[MD or PA]",
  "age": "[from Q2 or --age]",
  "enrollment_status": "[from Q2]",
  "medical_usage": "[from Q3]",
  "estimated_annual_visits": "[derived: light=3, moderate=8, heavy=15, uncertain=8]",
  "priorities": ["[from Q4]"],
  "provider_assignment": "[from Q5 or 'mostly accept']",
  "specialist_usage": "[derived from usage + priorities]"
}
```

### Phase 2: Discovery Brief & Approval

1. **Show Discovery Brief**:
```
MEDIGAP PLAN SELECTION BRIEF
===============================
Location: [state] ([zip])
Age: [age] — [enrollment status]
Medical Usage: [usage level] (~[visits] visits/year)
Priorities: [from Q4]
Provider Assignment: [from Q5]

Research agents will analyze:
- Current Plan G & Plan N premiums from 8-10 insurers (premium-researcher)
- State rules: birthday rule, switching, guaranteed issue (state-rules-analyst)
- Break-even analysis, excess charges, cost scenarios (claims-pattern-analyst)

Estimated time: 10-15 minutes
```

2. **APPROVAL GATE**: Ask the user to confirm before proceeding. Present the brief and wait for a go-ahead.

### Phase 3: Pre-Seed Research

Before dispatching agents, do 2-3 quick WebSearch queries to gather context:
- `medigap plan G plan N premiums [zip] [state] 2026`
- `[state] medigap birthday rule switching rules`
- `medicare "excess charges" prevalence [state]`

Use these results to seed agent prompts with initial context.

### Phase 4: Agent Dispatch

Read the 3 agent definition files, then launch all 3 agents simultaneously in a SINGLE message using `Task` with `run_in_background: true`:

| Agent | Subagent Type | Model | Searches | Focus |
|-------|--------------|-------|----------|-------|
| premium-researcher | general-purpose | opus | 10-15 | Premiums from 8-10 insurers, AM Best, NAIC, rate history |
| state-rules-analyst | general-purpose | sonnet | 8-12 | Birthday rule, switching, OEP, guaranteed issue |
| claims-pattern-analyst | general-purpose | sonnet | 8-12 | Break-even, excess charges, scenarios, projections |

**For each agent prompt, include**:
1. The agent's full instructions (read from `agents/[agent-name].md` relative to this command)
2. The Requirements Profile JSON from the interview
3. Any pre-seed research results
4. Instruction to return structured JSON with findings

### Phase 5: Synthesis

1. **Collect results**: Use `TaskOutput` with `block=true` for each agent. Handle failures gracefully — if an agent fails, note it in the final output and proceed with available results.

2. **Launch recommendation-synthesizer**: Use `Task` (subagent_type: `general-purpose`, model: `sonnet`) with:
   - The synthesizer's full instructions (read from `agents/recommendation-synthesizer.md`)
   - All 3 agent outputs concatenated
   - The Requirements Profile JSON

3. **Collect synthesis**: The synthesizer writes to `/tmp/medigap_selection.json`.

### Phase 6: Display Results

Present the results in chat:

```
## Medigap Plan Selection: [State] ([Zip])

**Date**: YYYY-MM-DD | **Age**: [age] | **Usage**: [usage level]

### Your Profile
- Location: [state] ([zip]) | Age: [age] ([enrollment status])
- Usage: [medical_usage] (~[visits] visits/year)
- Priorities: [priorities joined]
- Provider Assignment: [assignment status]

### Recommendation

**Winner: Plan [G/N]** — Suitability Score: [score]/100 (Confidence: [HIGH/MEDIUM/LOW])

> [one_line_summary]

| Factor | Plan G | Plan N |
|--------|--------|--------|
| Cost Efficiency (30%) | [score] | [score] |
| Risk Protection (25%) | [score] | [score] |
| Flexibility (20%) | [score] | [score] |
| Priority Alignment (15%) | [score] | [score] |
| Insurer Quality (10%) | [score] | [score] |
| **Composite** | **[G score]** | **[N score]** |

### Premium Comparison

| Insurer | Plan G | Plan N | Spread | AM Best | NAIC |
|---------|--------|--------|--------|---------|------|
| [insurer] | $[G]/mo | $[N]/mo | $[diff] | [rating] | [ratio] |
| ... | ... | ... | ... | ... | ... |

### Break-Even Analysis
- Monthly premium spread: $[spread]
- Office visits to break even: [N] visits/year
- Your estimated visits: [N]/year
- Excess charge risk: [level]

### Scenario Comparison

| Scenario | Plan G | Plan N | Winner | Savings |
|----------|--------|--------|--------|---------|
| Healthy Year | $[cost] | $[cost] | [winner] | $[amount] |
| Typical Year | $[cost] | $[cost] | [winner] | $[amount] |
| Bad Year | $[cost] | $[cost] | [winner] | $[amount] |
| Worst Case | $[cost] | $[cost] | [winner] | $[amount] |

### State Rules: [State]
- Birthday Rule: [Yes/No] — [explanation]
- Switching Strategy: [recommendation]

### Top Insurer Recommendation
**#1: [Insurer Name]** — $[premium]/month ([Plan])
- AM Best: [rating] | NAIC: [ratio] | Avg increase: [%]/year
- [Why recommended]

### Strategic Advice
1. [Advice item 1]
2. [Advice item 2]
3. [Advice item 3]

### Next Steps
- Compare insurers: `/medigap-selector:medigap-compare [Insurer1] vs [Insurer2]`
- Recall results: `/medigap-selector:medigap-results`
- Export to PDF/HTML: Request export
- Get official quotes: Visit Medicare.gov Plan Finder

> **Disclaimer**: This is not financial or medical advice. Consult with a licensed insurance agent or Medicare counselor (SHIP: [phone]). Always verify premiums through Medicare.gov Plan Finder.
```

### Phase 7: Export (optional)

If the user requests export:
```bash
~/.claude/scripts/.venv/bin/python3 [plugin_scripts_dir]/medigap_selector_export.py --input /tmp/medigap_selection.json
```

Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Medigap_Selection/`

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate data, statistics, premiums, or ratings.
- Present the Discovery Brief and wait for approval before dispatching agents.
- Handle agent failures gracefully — proceed with available results and note gaps.
- Always include the "not financial/medical advice" disclaimer.
- Always recommend verifying with Medicare.gov Plan Finder and SHIP counselor.
- Part B deductible ($283/year) is not covered by either plan — always mention this.
- The birthday rule (MD) fundamentally changes the recommendation — give it prominence.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Medigap_Selection/`
