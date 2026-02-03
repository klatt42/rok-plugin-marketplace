---
name: rpi-methodology
description: |
  Research-Plan-Implement (R-P-I) development methodology for structured
  software engineering. Enforces cognitive discipline: research before deciding,
  plan before building, implement with validation. Includes complexity assessment
  (SIMPLE/MEDIUM/COMPLEX) and pre-implementation protocol.
triggers:
  - "research first"
  - "plan this"
  - "implement plan"
  - "complexity assessment"
  - "pre-implementation"
version: 1.0
author: ROK Copilot
---

# R-P-I Methodology

## Three Phases

### Phase 1: Research (/1_research)
- Gather information WITHOUT making decisions
- Read relevant files, search codebase, check docs
- Output: research document with findings
- Rule: No implementation, no opinions, just facts

### Phase 2: Plan (/2_plan)
- Create implementation blueprint FROM research
- Present 2-3 approaches with trade-offs
- Get user approval before proceeding
- Output: step-by-step plan with file changes

### Phase 3: Implement (/3_implement)
- Execute the approved plan EXACTLY
- Track progress with TodoWrite
- Validate each step before moving on
- Output: working implementation with tests

## Complexity Assessment

| Level | Criteria | Action |
|-------|----------|--------|
| SIMPLE | Single file, <50 lines, clear pattern | Proceed directly |
| MEDIUM | Multiple files, some ambiguity | 2+ approaches minimum |
| COMPLEX | Architecture, unfamiliar, high risk | Full Pre-Implementation Protocol |

**Always COMPLEX**: Auth, payments, data migration, production risk

## Pre-Implementation Protocol (COMPLEX tasks)

1. State assumptions explicitly
2. Identify 3+ approaches
3. Evaluate trade-offs
4. Get user approval
5. Implement incrementally
6. Validate at each step
