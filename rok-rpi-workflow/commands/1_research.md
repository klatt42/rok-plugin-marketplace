# /1_research - R-P-I Phase 1: Research

Gathers all relevant information for a feature without making implementation decisions. Includes Feynman Checkpoint for understanding validation.

**Version**: 2.0 (ROK 3.6-Feynman)

## What This Does

1. **Defines Scope**: Clarifies research boundaries
2. **Explores Codebase**: Finds relevant files, patterns, and structure
3. **Searches Documentation**: Locates relevant docs and references
4. **Identifies Options**: Documents possible approaches (NOT recommendations)
5. **Surfaces Constraints**: Dependencies and limitations
6. **Runs Feynman Checkpoint**: Validates understanding before handoff

## Usage

```
/1_research <feature description>
```

## Execution Steps

### 1. Initialize Research

```
═══════════════════════════════════════════════════════
R-P-I WORKFLOW: PHASE 1 - RESEARCH
═══════════════════════════════════════════════════════

Feature/Problem: [description]
Started: [timestamp]
Output will be: thoughts/shared/research/[feature]-research.md

RESEARCH BOUNDARIES:
• DO: Gather information, identify options, document constraints
• DO NOT: Make implementation decisions, write code, recommend approaches

═══════════════════════════════════════════════════════
```

### 2. Research Scope Definition

```
RESEARCH SCOPE
──────────────
Primary question to answer:
→ [what we need to know]

Success criteria (research is complete when):
→ [specific completion markers]

Out of scope for this research:
→ [what we're NOT investigating]

Time/depth limit:
→ [bounds on research effort]
```

### 3. Execute Research

#### Internal Research
```
CODEBASE ANALYSIS
─────────────────
Related existing code:
• [file]: [relevance]

Patterns already in use:
• [pattern]: [where used]

Architectural constraints:
• [constraint]: [source]

Test coverage in area:
• [current state]
```

#### External Research
```
DOCUMENTATION REVIEW
────────────────────
Official docs consulted:
• [source]: [key findings]

PRIOR ART
─────────
Similar solutions found:
• [source]: [approach taken]

Common patterns:
• [pattern]: [pros/cons as observed]
```

### 4. Feynman Checkpoint (CRITICAL)

Before completing research:

```
FEYNMAN CHECKPOINT: Can I explain this simply?
──────────────────────────────────────────────

Main finding in plain language (no jargon):
→ [explanation a junior dev would understand]

Technical terms used - definitions:
• [term]: [simple definition]
• [term]: [simple definition]

Gaps in my understanding:
→ [what I still don't fully grasp]

If gaps exist: [continue research | flag for planner]
```

**If you cannot explain simply, you don't understand well enough to hand off.**

### 5. Generate Research Output

Create `thoughts/shared/research/[feature]-research.md`:

```markdown
# Research: [Feature Name]

**Date**: [timestamp]
**Researcher**: Claude (researcher agent)
**Status**: COMPLETE / INCOMPLETE - [reason]
**Feynman Check**: PASSED / GAPS NOTED

## Research Question
[What we needed to know]

## Current State
[What exists now in the codebase]

## Constraints Discovered
| Constraint | Source | Impact |
|------------|--------|--------|
| [what] | [where found] | [how it affects options] |

## Options Identified
*Note: These are options found, NOT recommendations*

### Option A: [Name]
- Description: [what it is]
- Where seen: [prior art source]
- Apparent pros: [observed benefits]
- Apparent cons: [observed drawbacks]
- Unknowns: [what's unclear]

### Option B: [Name]
[same structure]

### Option C: [Name]
[same structure]

## Feynman Check
Main finding in plain language:
→ [explanation]

Technical terms defined:
→ [term]: [simple definition]

Understanding gaps:
→ [gaps or "None"]

## Open Questions
- [ ] [question needing resolution]
- [ ] [question needing resolution]

## Key Files/References
| File/URL | Relevance |
|----------|-----------|
| [path or link] | [why it matters] |

## Raw Notes
[Detailed findings organized by source]

---
*Research complete. Ready for /2_plan*
```

### 6. Handoff

```
═══════════════════════════════════════════════════════
RESEARCH PHASE COMPLETE
═══════════════════════════════════════════════════════

Output: thoughts/shared/research/[feature]-research.md
Confidence: [HIGH/MEDIUM/LOW]
Open questions: [count]
Feynman Check: [PASSED/GAPS NOTED]

NEXT STEP:
Review research output, then:
  /2_plan thoughts/shared/research/[feature]-research.md

NOTE: Planner will make implementation decisions.
Research deliberately does NOT recommend approaches.
═══════════════════════════════════════════════════════
```

## Core Principle

**Gather, don't decide.** This phase collects information. Implementation decisions happen in Phase 2 (Plan).

## Important Rules

### DO
- Explore thoroughly before concluding
- Quote existing code patterns
- Note ALL relevant files found
- Surface constraints early
- Complete Feynman Checkpoint
- Ask clarifying questions if needed

### DON'T
- Make implementation decisions
- Write new code
- Recommend specific approaches
- Skip documenting constraints
- Assume—verify in codebase
- Skip Feynman Checkpoint

## Directory Setup

```bash
mkdir -p thoughts/shared/research
mkdir -p thoughts/shared/plans
mkdir -p thoughts/shared/expertise
mkdir -p thoughts/shared/progress
```

---

**Research Command v2.0** | ROK 3.6-Feynman with Explain Simply Checkpoint
