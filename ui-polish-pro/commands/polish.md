---
name: polish
description: |
  Master orchestration command for full UI/UX overhaul. Creates an isolated git
  branch, audits the entire app, extracts/generates a design system, polishes
  routes in parallel, validates the build, and generates a report. Use this for
  comprehensive visual upgrades of existing applications.
user_invocable: true
---

# /ui-polish-pro:polish

## Usage

```
/ui-polish-pro:polish [repo_path]
```

- `repo_path` — path to the project root (defaults to current working directory)
- Options: `--skip-worktree` (make changes on current branch), `--aiso` (include AISO patterns for public pages)

## Master Workflow

You are the orchestrator for the ui-polish-pro pipeline. Execute these phases in order, with HITL gates where specified.

### Phase 0: Isolation (Git Worktree)

1. Verify `repo_path` is a git repository
2. Get the current branch name: `git rev-parse --abbrev-ref HEAD`
3. Create an isolated worktree:
   ```bash
   TIMESTAMP=$(date +%s)
   PROJECT=$(basename {repo_path})
   BRANCH="ui-polish/${PROJECT}"
   git worktree add .claude/worktrees/ui-polish-${TIMESTAMP} -b ${BRANCH}
   ```
4. All subsequent work happens in the worktree directory
5. If `--skip-worktree` flag is set, skip this phase and work directly on the current branch

**Tell the user**: "Working on isolated branch `{BRANCH}`. Your original code is untouched."

### Phase 1: Deep Audit

Dispatch the `ui-auditor` agent:
- Input: `repo_path` (the worktree path)
- Wait for the UI Audit Brief JSON
- Present key findings to the user:
  - Overall score
  - Number of routes found
  - Top 3-5 opportunities
  - Missing libraries that will be installed

**HITL Gate 1**: Ask the user:
> "The audit found {N} routes scoring {score}/10 overall. Top opportunities: {list}. Which routes should I polish? (all high-priority / specific routes / all routes)"

### Phase 2: Design System

Dispatch the `design-extractor` agent:
- Input: `repo_path`, `audit_brief`
- Wait for the proposed design system JSON

**HITL Gate 2**: Present the design system to the user:
> "Here's the proposed design system based on your existing code:
> - Primary: {color}
> - Typography: {font} with {scale}
> - Spacing: {rhythm}
> - Border radius: {standard}
>
> Approve this system, or tell me what to change."

Wait for user approval or adjustments before proceeding.

### Phase 3: Install Dependencies

Before polishing, install any missing libraries in the worktree:

```bash
cd {worktree_path}
# Detect package manager
if [ -f "bun.lockb" ]; then PKG="bun"; elif [ -f "pnpm-lock.yaml" ]; then PKG="pnpm"; elif [ -f "yarn.lock" ]; then PKG="yarn"; else PKG="npm"; fi

# Install framer-motion if not present
if ! grep -q "framer-motion" package.json; then
  $PKG add framer-motion
fi

# Install lenis if smooth scroll is desired
# (only if user approves in Phase 2)
```

### Phase 4: Route-by-Route Polish

For each approved route (up to 4 in parallel):
1. Dispatch a `route-polisher` agent with:
   - `route_file` — the file path
   - `design_system` — the approved system
   - `audit_entry` — this route's audit data
   - `animation_patterns` — load the ui-animation skill content
2. Collect results from each agent

**Tell the user** progress as each route completes:
> "Polished /dashboard (3.8 -> 7.2). 3 of 5 routes complete..."

### Phase 5: Verification

Dispatch the `visual-validator` agent:
- Input: `repo_path`, `original_branch`, `polished_routes`
- Wait for validation results

If validation **fails**:
- Report the specific failures to the user
- Ask whether to fix and re-validate, or skip the failing routes

If validation **passes** or **warns**:
- Proceed to Phase 6

### Phase 6: Commit and Report

1. Commit all changes in the worktree:
   ```bash
   cd {worktree_path}
   git add -A
   git commit -m "ui-polish: production UI/UX overhaul

   - Polished {N} routes with entrance animations, hover states, and design system compliance
   - Added framer-motion for cinema-quality animations
   - Unified design tokens (colors, typography, spacing, radius)
   - Added accessibility: focus rings, reduced-motion support, ARIA labels
   - Overall score: {before} -> {after} ({grade})

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
   ```

2. Dispatch the `report-generator` agent:
   - Input: all pipeline outputs
   - Wait for the report

3. Present final summary to user:
   > "UI polish complete!
   > - Routes polished: {N}
   > - Overall score: {before} -> {after} ({grade})
   > - Branch: {BRANCH}
   > - Report: {report_path}
   >
   > To merge: `git checkout main && git merge {BRANCH}`
   > To review: `git diff main...{BRANCH}`"

## Error Handling

- If git worktree creation fails (dirty working tree): suggest `git stash` first
- If build fails after polish: report errors, offer to revert specific routes
- If a route-polisher agent fails: skip that route, continue with others
- If no routes found: suggest the user specify the routes directory manually

## Rules

- Always create an isolated branch unless `--skip-worktree` is explicitly set
- Never skip HITL gates — user approval on design system is mandatory
- Polish in parallel (up to 4 routes) for speed
- Keep the user informed of progress throughout
- If the overall score doesn't improve by at least 2 points, flag it and ask if the user wants to iterate
