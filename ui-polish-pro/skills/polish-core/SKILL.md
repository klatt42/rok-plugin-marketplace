---
name: polish-core
description: |
  Master workflow orchestration for ui-polish-pro. Defines the 6-phase pipeline
  (isolation, audit, design system, polish, verification, report), HITL gates,
  agent dispatch patterns, and error recovery. Load this when running /polish.
triggers:
  - "ui polish"
  - "polish workflow"
  - "visual overhaul"
  - "production ui"
version: 1.0
author: ROK Agency
---

# Polish Core - Master Workflow

## Pipeline Overview

```
Phase 0: Isolation     -> git worktree (isolated branch)
Phase 1: Deep Audit    -> ui-auditor agent (read-only scan)
       [HITL Gate 1]   -> User approves scope
Phase 2: Design System -> design-extractor agent
       [HITL Gate 2]   -> User approves tokens
Phase 3: Dependencies  -> Install framer-motion, lenis
Phase 4: Route Polish  -> route-polisher agents (parallel, up to 4)
Phase 5: Verification  -> visual-validator agent (build + diff check)
Phase 6: Report        -> report-generator agent + commit
```

## Agent Dispatch Reference

### ui-auditor (Phase 1)
- **Model**: opus (needs deep analysis capability)
- **Tools**: Glob, Grep, Read
- **Input**: `repo_path`
- **Output**: UI Audit Brief JSON
- **Timeout**: Allow up to 5 minutes for large codebases

### design-extractor (Phase 2)
- **Model**: sonnet (pattern extraction, not creative)
- **Tools**: Glob, Grep, Read
- **Input**: `repo_path`, `audit_brief`, `mode: extract|generate`
- **Output**: Design System JSON

### route-polisher (Phase 4, parallel)
- **Model**: sonnet (code generation)
- **Tools**: Read, Write, Edit
- **Input**: `route_file`, `design_system`, `audit_entry`, `animation_patterns`
- **Output**: Change summary JSON
- **Parallelism**: Up to 4 concurrent agents
- **Critical**: Each agent MUST receive the ui-animation skill content

### visual-validator (Phase 5)
- **Model**: sonnet (verification)
- **Tools**: Bash, Read, Glob, Grep
- **Input**: `repo_path`, `original_branch`, `polished_routes`
- **Output**: Validation results JSON

### report-generator (Phase 6)
- **Model**: sonnet (synthesis)
- **Tools**: Read, Write, Bash
- **Input**: All pipeline outputs
- **Output**: Report files (MD/PDF/HTML)

## HITL Gates

Two mandatory human-in-the-loop checkpoints:

### Gate 1: Scope Approval (after Phase 1)
Present:
- Overall score
- Route count and breakdown by priority
- Top opportunities
- Missing libraries to install

Ask: "Which routes should I polish?"
Options: all high-priority / specific routes / all routes / cancel

### Gate 2: Design System Approval (after Phase 2)
Present:
- Color palette (primary, secondary, accent, semantic)
- Typography scale
- Spacing rhythm
- Border radius standard
- Shadow scale

Ask: "Approve this design system, or tell me what to change."
Iterate until approved.

## Error Recovery

| Failure | Recovery |
|---------|----------|
| Worktree creation fails | Suggest `git stash`, or use `--skip-worktree` |
| Audit finds 0 routes | Ask user to specify routes directory |
| Route polisher fails | Skip that route, continue others, report partial |
| Build fails after polish | Report error, offer to revert specific routes |
| Type errors introduced | Report errors with file:line, ask to fix or revert |
| Score doesn't improve 2+ pts | Flag it, ask if user wants to iterate |

## Parallel Dispatch Pattern

For Phase 4, dispatch route-polisher agents using the Agent tool:

```
For each route in approved_routes (max 4 concurrent):
  Agent(
    subagent_type="route-polisher",
    prompt="Polish {route_file} using design system: {json}...",
    model="sonnet",
    isolation="worktree" // NOT needed - already in worktree
  )
```

Wait for all agents to complete before Phase 5.

## Quality Thresholds

| Metric | Minimum | Target |
|--------|---------|--------|
| Overall score improvement | +3.0 points | +4.0 points |
| Build status | PASS | PASS |
| Functional code preserved | 100% | 100% |
| Accessibility score | +2.0 points | +3.0 points |
| Animation layers per route | 3 (page/section/item) | 4+ (+ hover/interaction) |
| Transformation categories per route | 5 minimum | 7+ |
| Visual difference | Obvious at a glance | "Looks like a different app" |

**If a polished route scores below +3.0 improvement, the polisher did not do enough.** The route-polisher agent is instructed to make dramatic, visible transformations across layout, typography, color, animation, interactivity, and accessibility — not subtle tweaks.

## Context Budget

Estimated token usage per full pipeline run:
- Phase 1 (audit): ~15K tokens
- Phase 2 (design): ~8K tokens
- Phase 4 (polish): ~20K per route x N routes (higher due to full rewrites)
- Phase 5 (validate): ~10K tokens
- Phase 6 (report): ~8K tokens

For a 5-route app: ~130K total tokens. Fits within a single Opus session.
