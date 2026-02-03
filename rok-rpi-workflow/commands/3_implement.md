---
name: implement
description: R-P-I Phase 3 - Execute approved plan with self-validation
version: 2.2
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "~/.claude/hooks/validators/json_validator.py"
          timeout: 5
        - type: command
          command: "~/.claude/hooks/validators/typescript_lint.sh"
          timeout: 30
  Stop:
    - type: command
      command: "~/.claude/hooks/validators/build_check.sh"
      timeout: 120
---

# /3_implement - R-P-I Phase 3: Implement

Executes approved implementation plan step-by-step, with per-step complexity assessment and real-time learning capture.

**Version**: 2.2 (ROK 3.8 + Context Reset Protocol + Self-Validation Hooks)

## What This Does

1. **Context Reset Check**: Ensures clean context for maximum reasoning room
2. **Verifies Approval**: Confirms plan has been approved
3. **Checks Prerequisites**: Validates requirements before starting
4. **Assesses Per-Step**: Complexity check for each step
5. **Executes Steps**: Implements each step as specified
6. **Captures Real-Time**: Assumption corrections as discovered
7. **Reports Progress**: Continuous status updates
8. **Generates Learnings**: Structured expertise extraction

## Context Reset Protocol (NEW - Cole Pattern)

> "We want to keep our context as light as possible when we get into the actual coding to leave as much room for the agent to reason." - Cole Medin

### Pre-Implementation Context Check

Before starting implementation:

```
═══════════════════════════════════════════════════════
CONTEXT RESET CHECK
═══════════════════════════════════════════════════════

Context usage: [estimate current usage]%

If context > 50%:
  RECOMMENDATION: Run /clear or start fresh session

  Reason: Planning phase explored many options, loaded
  context, and debated approaches. Implementation needs
  clean headroom for actual coding work.

  Action: Copy plan path, clear context, read ONLY:
  1. The approved plan file
  2. Files to be modified (on-demand)

  DO NOT reload:
  - PRD (already captured in plan)
  - Research docs (already synthesized)
  - Conversation history (plan has decisions)

If context < 50%:
  OK to proceed with current context

═══════════════════════════════════════════════════════
```

### Minimal Context Implementation

When implementing after reset:

```
READ ONLY:
1. The approved plan file (once)
2. Each file to modify (as needed)
3. Reference docs (only if stuck)

DO NOT READ:
- Full PRD (plan has relevant scope)
- Research output (plan has synthesis)
- Previous conversation (plan has decisions)

RATIONALE:
Every token spent on context = token NOT available for reasoning
Plan already contains everything needed to implement
```

## Usage

```
/3_implement <path-to-approved-plan>
```

Example:
```
/3_implement thoughts/shared/plans/voice-history-plan.md
```

## Core Principle

**Execute the plan, capture while doing.** Implementation reveals what planning couldn't predict. Capture assumption corrections in real-time.

## Execution Steps

### 1. Initialize Implementation

```
═══════════════════════════════════════════════════════
R-P-I WORKFLOW: PHASE 3 - IMPLEMENT
═══════════════════════════════════════════════════════

Plan input: [file path]
Started: [timestamp]
Progress log: thoughts/shared/progress/[feature]-progress.md
Learnings output: thoughts/shared/expertise/[feature]-learnings.md

IMPLEMENTATION PROTOCOL: Per-Step Assessment
Rationale: Each step may reveal unknowns not visible in planning.
           Capture corrections immediately, not at session end.

═══════════════════════════════════════════════════════
```

### 2. Verify Approval (MANDATORY)

```
APPROVAL CHECK
──────────────
Plan: [file path]
Status: [reading status field...]

☐ Status is "Approved" (not "Awaiting Approval")
☐ Approval timestamp exists
☐ No unresolved concerns noted

If not approved: STOP and return to /2_plan for approval.
```

### 3. Check Prerequisites

```
PREREQUISITE VERIFICATION
─────────────────────────
From plan:

| # | Prerequisite | Status | Check |
|---|--------------|--------|-------|
| 1 | | ☐ Met / ☐ Not Met | |
| 2 | | | |

If prerequisites not met: STOP and resolve before continuing.
```

### 4. Execute Steps with Per-Step Assessment

For EACH step in the plan:

#### Step 4.1: Pre-Step Complexity Check

```
═══════════════════════════════════════════════════════
STEP [N]: [Step Name]
═══════════════════════════════════════════════════════

COMPLEXITY QUICK-CHECK:
• Unknowns in this step? [yes/no]
• External dependencies? [yes/no]
• Multiple ways to implement? [yes/no]

PROTOCOL: [SIMPLE - execute | MEDIUM - pause and verify | COMPLEX - mini-plan first]
```

#### Step 4.2: Execute Step

```
EXECUTING STEP [N]
──────────────────
File(s): [paths]
Action: [Create/Modify/Delete]

[Actual implementation work happens here]

RESULT:
• Status: [Complete/Failed/Partial]
• Changes made: [summary]
• Verification: [command run and result]
```

#### Step 4.3: Real-Time Assumption Capture (CRITICAL)

After EACH step, check:

```
ASSUMPTION CHECK (Step [N])
───────────────────────────
Did anything surprise me in this step?

☐ No surprises - assumptions held
☐ YES - Assumption correction needed:

| What I Assumed | What Was True | Impact |
|----------------|---------------|--------|
| | | |

[If correction found, add to progress log immediately]
```

### 5. Progress Tracking

Maintain `thoughts/shared/progress/[feature]-progress.md`:

```markdown
# Progress: [Feature Name]

**Started**: [timestamp]
**Plan**: [path]
**Last Updated**: [timestamp]

## Status
- Current Phase: [N] of [Total]
- Current Step: [M] of [Total in Phase]
- Overall: [percentage]%

## Completed Steps
| Step | Name | Status | Time |
|------|------|--------|------|
| 1.1 | | ✓ | |
| 1.2 | | ✓ | |

## In Progress
Step [N.M]: [name]
Started: [timestamp]
Blockers: [none or description]

## Assumption Corrections (Real-Time)
| Step | Assumption | Correction | Action Taken |
|------|------------|------------|--------------|
| 1.2 | | | |

## Deviations from Plan
| Step | Planned | Actual | Reason |
|------|---------|--------|--------|
```

### 6. Handle Deviations

When step cannot be executed as planned:

```
═══════════════════════════════════════════════════════
⚠️ DEVIATION DETECTED
═══════════════════════════════════════════════════════

Step: [N.M] [Step Name]

PLANNED (from approved plan):
→

ACTUAL (what happened):
→

REASON:
→

ASSUMPTION CORRECTION:
| What I Assumed | What Was True |
|----------------|---------------|
| | |

═══════════════════════════════════════════════════════
DECISION REQUIRED:

Options:
1. MINOR FIX: [describe fix if safe and obvious]
2. RETURN TO PLANNING: Plan needs revision
3. USER INPUT: Need guidance on approach

Recommendation: [1/2/3] because [reason]

⏸️ Awaiting decision before continuing...
═══════════════════════════════════════════════════════
```

**Rule**: Do NOT improvise major changes. Report and wait.

### 7. Phase Checkpoints

After completing each phase:

```
═══════════════════════════════════════════════════════
PHASE [N] CHECKPOINT
═══════════════════════════════════════════════════════

Completed Steps:
✓ [N].1: [name]
✓ [N].2: [name]
✓ [N].3: [name]

Verification:
Command: [verification command from plan]
Result: [output]
Status: ✓ PASSED / ✗ FAILED

Assumption Corrections This Phase: [count]
Progress: [N] of [Total] phases complete ([percentage]%)

═══════════════════════════════════════════════════════
```

### 8. Completion Report

```
═══════════════════════════════════════════════════════
✅ IMPLEMENTATION COMPLETE
═══════════════════════════════════════════════════════

# Implementation Report: [Feature Name]

**Date**: [timestamp]
**Plan**: thoughts/shared/plans/[feature]-plan.md
**Duration**: [time from start]
**Implementer**: Claude (implementer agent)

## Summary
[What was built in 2-3 sentences]

## Phases Completed

| Phase | Name | Steps | Status |
|-------|------|-------|--------|
| 1 | | | ✓ |
| 2 | | | ✓ |
| 3 | | | ✓ |

## Files Changed

| File | Action | Lines |
|------|--------|-------|
| | Created/Modified/Deleted | |

## Verification Results

- [x] Type check: ✓
- [x] Tests: ✓
- [x] Manual verification: [result]

## Success Criteria (from plan)

- [x] [Criterion 1]
- [x] [Criterion 2]

## Assumption Corrections Summary

Total corrections captured: [count]

| # | Assumption | Correction | Future Guidance |
|---|------------|------------|-----------------|
| 1 | | | |

═══════════════════════════════════════════════════════
```

### 9. Generate Learnings File (MANDATORY)

Create `thoughts/shared/expertise/[feature]-learnings.md`:

```markdown
# Implementation Learnings: [Feature Name]

**Date**: [timestamp]
**Plan Source**: thoughts/shared/plans/[feature]-plan.md
**Implementation Duration**: [time]
**Status**: Complete

## What Worked Well
- [Successful approach that should be repeated]
- [Pattern that made implementation smooth]

## Assumption Corrections Captured

| What I Assumed | What Was True | How I Discovered | Future Guidance |
|----------------|---------------|------------------|-----------------|
| | | | |

## Challenges Encountered

| Challenge | Resolution | Prevention |
|-----------|------------|------------|
| | | |

## Patterns for Reuse

### Pattern: [Name]
- **When to use**: [context]
- **Implementation**: [how]
- **Example from this session**: [reference]

## Anti-Patterns Avoided/Encountered

- [x/unchecked] Pattern Matching without verification
- [x/unchecked] Premature implementation
- [x/unchecked] Assumption skipping
- [x/unchecked] Other: [describe]

## Recommendations for Similar Work

1. [Specific recommendation]
2. [Specific recommendation]

## Files to Review for Similar Features

| File | Relevance |
|------|-----------|
| | |

---

*Generated by /3_implement v2.0 | ROK 3.6-Feynman*
*Ready for /reflect synthesis*
```

### 10. Handoff

```
═══════════════════════════════════════════════════════
IMPLEMENTATION PHASE COMPLETE
═══════════════════════════════════════════════════════

Progress log: thoughts/shared/progress/[feature]-progress.md
Learnings: thoughts/shared/expertise/[feature]-learnings.md
Assumption corrections: [count] captured

NEXT STEPS:
• Run /diary to capture session-level learnings
• Run /reflect weekly to synthesize into CLAUDE.md
• Review learnings file for pattern extraction

ARTIFACTS CREATED:
• [feature] implementation complete
• [count] files created/modified
• [count] tests passing
• [count] assumption corrections documented

═══════════════════════════════════════════════════════
```

## Important Rules

### DO
- Verify approval before starting
- Run per-step complexity assessment
- Capture assumption corrections in real-time
- Run verification after each step
- Update progress file continuously
- Complete learnings file

### DON'T
- Execute without approval
- Skip per-step assessment
- Wait until end to capture learnings
- Deviate from plan without permission
- Continue after failures silently
- Add features beyond plan scope

## Multi-Session Implementations

For implementations spanning multiple sessions:

**Save checkpoint:**
```
Update thoughts/shared/progress/[feature]-progress.md with:
- Current step
- All completed steps
- Any blockers
- Assumption corrections so far
```

**Resume:**
```
/3_implement thoughts/shared/plans/[feature]-plan.md

Reads progress file and continues from last checkpoint.
```

## Error Reference

### Compilation Error
```
✗ Step [N.M]: Compilation failed

Error: [message]
File: [file]:[line]

ASSUMPTION CHECK:
What did the plan assume that wasn't true?
→ [analysis]

Awaiting instruction...
```

### Test Failure
```
✗ Step [N.M]: Tests failed

Failed: [test name]
Expected: [expected]
Actual: [actual]

ASSUMPTION CHECK:
What assumption about behavior was wrong?
→ [analysis]

Awaiting instruction...
```

### Missing Dependency
```
✗ Step [N.M]: Missing dependency

Required: [what]
Status: Not available

ASSUMPTION CHECK:
Plan assumed [X] but [Y] is true.

Awaiting instruction...
```

---

**Implement Command v2.0** | ROK 3.6-Feynman Real-Time Learning Capture
