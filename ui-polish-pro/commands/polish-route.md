---
name: polish-route
description: |
  Surgical polish of a single route or page file. No worktree needed - changes
  are small and reviewable. Ideal for iterative polish after a full pass, or for
  polishing individual landing pages and components.
user_invocable: true
---

# /ui-polish-pro:polish-route

## Usage

```
/ui-polish-pro:polish-route <file_path> [--design-system path/to/system.json]
```

- `file_path` — path to the specific TSX/JSX file to polish
- `--design-system` — optional path to a previously generated design system JSON

## Workflow

This is the lightweight, surgical version of `/ui-polish-pro:polish`. No worktree, no multi-agent orchestration — just focused improvement of a single file.

### Step 1: Read and Assess

1. Read the target file completely
2. Identify the framework context (Next.js app router, pages router, etc.)
3. Perform a quick 8-dimension score assessment (same rubric as full audit)
4. Identify the top 3-5 improvement opportunities

Present to the user:
> "Current score for `{file}`: {score}/10
> Top opportunities:
> 1. {opp_1}
> 2. {opp_2}
> 3. {opp_3}
>
> Shall I proceed with all improvements, or focus on specific areas?"

### Step 2: Load Design Context

If `--design-system` is provided:
- Read and use those tokens

If no design system is provided:
- Quick-scan the file and its imports for existing patterns
- Check for `tailwind.config.ts` in the project root
- Infer a mini design system from current usage
- Use sensible defaults where patterns are unclear

### Step 3: Polish

Dispatch the `route-polisher` agent (or act as one directly for speed). The transformation should be **visibly dramatic** — not subtle tweaks. Apply ALL of these categories that are relevant:

- **Page structure**: Add header sections with gradients, alternating section backgrounds, proper containers
- **Card/component redesign**: Shadow depth, hover lift, icon badges, trend indicators, group hover effects
- **Multi-layer animations**: Page entrance -> section stagger -> item stagger (3 timescales minimum)
- **Typography overhaul**: Size hierarchy, weight variation, tracking, color depth (not just one font-size change)
- **Button polish**: Gradient primaries with shadow, spring hover/tap, ghost secondaries with border hover
- **Table/list enhancement**: Styled headers, row stagger entrance, hover highlight rows
- **Empty state design**: Centered icon + title + description + CTA (not blank space)
- **Accessibility**: focus-visible rings, useReducedMotion, ARIA labels, semantic HTML
- **Design system compliance**: Normalize colors, spacing, radius, shadows to approved tokens

**Minimum 5 categories per route.** If someone can't tell the page changed at a glance, it's not enough.

### Step 4: Quick Verify

After changes:
1. Check for TypeScript errors in the modified file:
   ```bash
   npx tsc --noEmit {file_path} 2>&1
   ```
2. Show the user a summary of changes made
3. Show the before/after score

Present:
> "Polished `{file}`: {before} -> {after}/10
> Changes:
> - {change_1}
> - {change_2}
> ...
> Build check: {pass/fail}"

## When to Use This Command

- **After a full `/polish` pass**: iterating on specific routes that need more work
- **Single landing page**: e.g., polishing a genesis-landing-page-pro output
- **Quick fix**: adding animations or design system compliance to one page
- **Component polish**: improving a shared component (will affect all consumers)

## Rules

- Changes are made directly to the file (no worktree isolation)
- Still MUST preserve all functional code
- Show the user what changed before and after
- If the file is a server component and animations are needed, add `"use client"` and warn the user about the conversion
- Keep it fast — this should complete in under 2 minutes for a typical route
