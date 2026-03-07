---
name: audit-ui
description: |
  Standalone visual audit that produces a comprehensive UI quality report
  without making any code changes. Works on local codebases or deployed URLs.
  Use this for competitive analysis, pre-polish assessment, or auditing deployed sites.
user_invocable: true
---

# /ui-polish-pro:audit-ui

## Usage

```
/ui-polish-pro:audit-ui [target]
```

- `target` — either a local path or a URL
  - Local path: `/path/to/repo` or `.` (defaults to current directory)
  - URL: `https://example.com` (triggers browser-based visual audit)

### Mode 1: Local Codebase Audit

1. Dispatch the `ui-auditor` agent with `repo_path`
2. Wait for the UI Audit Brief JSON
3. Present a formatted report to the user

**Report format**:

```
## UI Audit Report: {projectName}

**Framework**: {framework}
**Overall Score**: {score}/10 ({grade})
**Routes Scanned**: {count}

### Scores by Route

| Route | Layout | Type | Color | Anim | Inter | Resp | A11y | Polish | Total |
|-------|--------|------|-------|------|-------|------|------|--------|-------|
| /     | 5      | 4    | 6     | 2    | 3     | 5    | 3    | 2      | 3.8   |
| /dash | 6      | 5    | 6     | 1    | 2     | 4    | 2    | 1      | 3.4   |

### Top Opportunities
1. {opportunity_1}
2. {opportunity_2}
3. {opportunity_3}

### Design Token Issues
- Colors: {color_issues}
- Typography: {type_issues}
- Spacing: {spacing_issues}

### Accessibility Gaps
- {gap_1}
- {gap_2}

### Recommended Next Step
Run `/ui-polish-pro:polish` to apply production-quality visual improvements.
```

### Mode 2: URL-Based Visual Audit

When the target starts with `http://` or `https://`:

1. Use browser automation to visit the URL:
   - If Claude in Chrome is available, use it for visual inspection
   - Otherwise, use playwright-cli or agent-browser for headless capture

2. Evaluate the live page visually on the 8-dimension rubric:
   - Layout & Spacing: visual rhythm, alignment, whitespace usage
   - Typography: heading hierarchy, readability, font quality
   - Color System: palette harmony, contrast, consistency
   - Animation & Motion: transitions, hover effects, scroll behavior
   - Interactivity: button feedback, form UX, loading states
   - Responsiveness: check at 375px, 768px, 1024px, 1440px
   - Accessibility: keyboard navigation, contrast ratios
   - Visual Polish: shadows, radius, micro-interactions, overall fit/finish

3. Present findings in the same report format as Mode 1, but without file-level detail

## Rules

- This command is **strictly read-only**. No files are created or modified (except the report output).
- For local audits, do not suggest or make changes — only analyze and report.
- For URL audits, respect rate limiting and don't hammer the target site.
- Score honestly. The goal is an accurate baseline, not flattery.
- If the target is a single-page app, treat each major section as a "route" for scoring purposes.
