# /2_plan - R-P-I Phase 2: Plan

Creates detailed implementation blueprint using FULL Feynman Pre-Implementation Protocol. Requires human approval before implementation.

**Version**: 2.0 (ROK 3.6-Feynman)

## What This Does

1. **Loads Research**: Reads research document as input
2. **Runs Full Protocol**: Essential Puzzle Reduction + 3 Approaches + Assumption Verification
3. **Selects Approach**: Documents rationale for chosen approach
4. **Creates Blueprint**: Phased, step-by-step implementation plan
5. **Requires Approval**: Human must approve before /3_implement

## Usage

```
/2_plan <path-to-research-document>
```

## Core Principle

**Planning is ALWAYS COMPLEX.** Wrong approach selection wastes significant effort. Full Pre-Implementation Protocol is mandatory.

## Execution Steps

### 1. Initialize Planning

```
═══════════════════════════════════════════════════════
R-P-I WORKFLOW: PHASE 2 - PLAN
═══════════════════════════════════════════════════════

Research input: [file path]
Started: [timestamp]
Output will be: thoughts/shared/plans/[feature]-plan.md

PLANNING PROTOCOL: COMPLEX (Full Feynman required)
Rationale: Planning decisions propagate to all implementation.
           Wrong approach selection wastes significant effort.

═══════════════════════════════════════════════════════
```

### 2. Consume Research

```
RESEARCH REVIEW
───────────────
Reading: [research file path]

Key findings:
• [summary point]

Constraints identified:
• [constraint]

Options found:
• Option A: [name]
• Option B: [name]
• Option C: [name]

Open questions (become assumptions to verify):
• [question]
```

### 3. Full Pre-Implementation Protocol (MANDATORY)

#### Step 3.1: Essential Puzzle Reduction

```
═══════════════════════════════════════════════════════
ESSENTIAL PUZZLE REDUCTION
═══════════════════════════════════════════════════════

PROBLEM STATEMENT (one sentence a junior dev would understand):
→

SIMPLEST POSSIBLE EXAMPLE:
→

SUCCESS CRITERIA (how to verify solution works):
→

THE CORE PUZZLE (what makes this actually hard?):
→

═══════════════════════════════════════════════════════
```

#### Step 3.2: Multi-Angle Decomposition (3 approaches minimum)

```
═══════════════════════════════════════════════════════
APPROACH A: [Name]
═══════════════════════════════════════════════════════
Description:

Key Assumptions:
1.
2.
3.

Risks:
1.
2.

Testing Strategy:


═══════════════════════════════════════════════════════
APPROACH B: [Name]
═══════════════════════════════════════════════════════
[same structure]

═══════════════════════════════════════════════════════
APPROACH C: [Name]
═══════════════════════════════════════════════════════
[same structure]
```

#### Step 3.3: Assumption Verification

```
═══════════════════════════════════════════════════════
ASSUMPTION VERIFICATION
═══════════════════════════════════════════════════════

| # | Assumption | Status | Evidence/Risk |
|---|------------|--------|---------------|
| 1 | | ☐ Verified / ☐ Assumed | |
| 2 | | | |
| 3 | | | |

UNVERIFIED ASSUMPTIONS ACCEPTED:
• [assumption]: Risk [LOW/MED/HIGH] - [rationale]

═══════════════════════════════════════════════════════
```

#### Step 3.4: Approach Selection

```
═══════════════════════════════════════════════════════
APPROACH SELECTION
═══════════════════════════════════════════════════════

SELECTED: Approach [A/B/C]

RATIONALE:


REJECTED - Approach [X]:
Reason:

REJECTED - Approach [Y]:
Reason:

RISKS ACCEPTED:


RECONSIDER IF:


═══════════════════════════════════════════════════════
```

### 4. Generate Implementation Blueprint

```markdown
# Implementation Plan: [Feature Name]

**Date**: [timestamp]
**Planner**: Claude (planner agent)
**Research source**: [path]
**Protocol**: Full Feynman Pre-Implementation
**Status**: Awaiting Approval

## Pre-Implementation Protocol Summary

### Essential Puzzle Reduction
[1-paragraph problem statement for junior dev]

### Approaches Considered
| Approach | Description | Selected? |
|----------|-------------|-----------|
| A | [desc] | No - [reason] |
| B | [desc] | **YES** |
| C | [desc] | No - [reason] |

### Key Assumptions Verified
| Assumption | Status | Evidence |
|------------|--------|----------|

---

## Selected Approach
**Name**: [approach name]
**Summary**: [one paragraph]

## Prerequisites
- [ ] [prerequisite 1]
- [ ] [prerequisite 2]

## Step-by-Step Implementation

### Step 1: [Name]
**Files affected**:
- [file path]

**Changes**:
[Detailed description]

**Verification**:
[How to confirm step is complete]

**Rollback**:
[How to undo if needed]

---

### Step 2: [Name]
[same structure]

---

## Testing Plan

### Unit Tests
- [ ] [test description]

### Integration Tests
- [ ] [test description]

### Manual Verification
1. [step]
2. [step]

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|

## Definition of Done
- [ ] All steps completed
- [ ] All tests passing
- [ ] [criterion]

---

**REQUIRES HUMAN APPROVAL BEFORE IMPLEMENTATION**
```

### 5. Human Checkpoint (MANDATORY)

```
═══════════════════════════════════════════════════════
PLAN READY FOR REVIEW
═══════════════════════════════════════════════════════

Plan location: thoughts/shared/plans/[feature]-plan.md

BEFORE APPROVING, VERIFY:
☐ Selected approach makes sense for your context
☐ Assumptions are acceptable risks
☐ Steps are appropriately granular
☐ Testing plan is sufficient
☐ No obvious gaps or concerns

TO APPROVE: Reply "Approved"
TO REVISE: Specify what needs changing

Awaiting approval before /3_implement
═══════════════════════════════════════════════════════
```

### 6. Handoff (After Approval)

```
═══════════════════════════════════════════════════════
PLAN APPROVED - READY FOR IMPLEMENTATION
═══════════════════════════════════════════════════════

Plan: thoughts/shared/plans/[feature]-plan.md
Approved: [timestamp]

NEXT STEP:
  /3_implement thoughts/shared/plans/[feature]-plan.md

IMPLEMENTATION RULES:
• Follow plan steps in order
• Reference ONLY the plan (not raw research)
• Capture learnings as you go
• Stop and reassess if plan proves wrong

═══════════════════════════════════════════════════════
```

## Important Rules

### DO
- Complete FULL Pre-Implementation Protocol
- Generate 3 approaches minimum
- Verify all assumptions explicitly
- Include every file change
- Define verification for every step
- Wait for explicit approval

### DON'T
- Skip any protocol steps
- Generate fewer than 3 approaches
- Leave assumptions unverified
- Leave steps vague
- Skip human approval
- Proceed without approval

---

**Plan Command v2.0** | ROK 3.6-Feynman Full Pre-Implementation Protocol
