---
description: Comprehensive pre-production code review with parallel subagents
argument-hint: [path/to/project] [--scope=full|focused] [--include=security,tests,...]
allowed-tools: Bash(git:*), Bash(npm:*), Bash(npx:*), Bash(find:*), Bash(wc:*), Bash(ls:*), Bash(python3:*), Read, Glob, Grep, Write, Task, TaskOutput, TodoWrite
---

# Production Code Review

Run a comprehensive, multi-dimensional code review before deploying to production (Netlify/Vercel). This is NOT a PR review -- it reviews the entire repository for production readiness.

## Usage

```
/production-code-review:review                              # Full review of cwd
/production-code-review:review /path/to/project             # Specific project
/production-code-review:review --scope=focused src/         # Focus on src/ only
/production-code-review:review --include=security,tests     # Only specific dimensions
```

## Arguments

- **path** (optional): Project directory. Default: current working directory.
- **--scope** (optional): `full` (default) or `focused` (only specified subdirectory).
- **--include** (optional): Comma-separated dimensions to run. Default: all. Options: `quality`, `tests`, `ui`, `responsive`, `security`, `performance`.

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Project Structure Scan

Before launching subagents, gather project intelligence:

1. **Identify tech stack**: Read `package.json`, `tsconfig.json`, framework configs
2. **Read project conventions**: Check for `CLAUDE.md` or `README.md`
3. **Count source files**: Estimate scope across key directories
4. **Check git status**: Branch, recent commits, dirty state
5. **Identify key directories**: `src/`, `app/`, `pages/`, `components/`, `lib/`, `api/`, `tests/`

Build a **Project Context Brief** to share with all agents:

```
PROJECT CONTEXT
===============
Name: [from package.json]
Path: [absolute path]
Stack: [Next.js 14 / React / Vite / etc.]
Framework: [App Router / Pages Router / etc.]
Styling: [Tailwind / CSS Modules / styled-components]
Testing: [Vitest / Jest / Playwright / Cypress / none]
Total Source Files: [count]
Key Directories: [list]
Deploy Target: [Netlify / Vercel / inferred]
Project Conventions: [from CLAUDE.md if present]
Scope: [full | focused on X]
```

### Phase 2: Dispatch 6 Specialized Agents in Parallel

Launch all 6 review agents simultaneously using `Task` with `run_in_background: true`. Each agent receives the Project Context Brief plus its dimension-specific instructions. **All agents should be dispatched in a single message for maximum parallelism.**

The 6 agents (determine which to launch based on --include flag, default all):

1. **code-quality-reviewer** (Opus) - DRY, SOLID, naming, structure, dead code
2. **test-coverage-reviewer** (Sonnet) - Coverage gaps, test quality, E2E
3. **ui-ux-reviewer** (Sonnet) - Contrast, fonts, images, accessibility
4. **responsive-design-reviewer** (Sonnet) - Breakpoints, mobile, touch targets
5. **security-reviewer** (Opus) - OWASP Top 10, secrets, injection
6. **performance-reviewer** (Sonnet) - Bundle size, N+1, memory leaks

Each agent prompt should include:
- The Project Context Brief from Phase 1
- The agent's specific review instructions (from its agent definition)
- The project path to review
- Instruction to return ONLY structured JSON in the required output format

Use `subagent_type: "general-purpose"` for all agents, embedding the agent's review instructions in the prompt.

### Phase 3: Collect and Synthesize Results

1. **Collect all results**: Use `TaskOutput` with `block: true` for each agent
2. **Parse JSON outputs**: Extract structured data from each agent response. If an agent wrapped its JSON in markdown code blocks, extract the JSON content.
3. **Handle failures**: If an agent timed out or failed, note as "incomplete" with score 50
4. **Filter issues**: Only include issues with `confidence >= 80`
5. **Deduplicate**: If multiple agents flag the same file:line, merge findings
6. **Calculate Production Readiness Score**:

```
weighted = (
  code_quality * 0.20 +
  testing * 0.20 +
  ui_ux * 0.15 +
  responsive * 0.15 +
  security * 0.20 +
  performance * 0.10
)

penalties = (critical_count * 10) + (high_count * 3)
final = max(0, min(100, round(weighted - penalties)))
```

7. **Determine Verdict**:
   - `final >= 85` AND `critical_count == 0`: **PASS**
   - `final >= 70` AND `critical_count == 0`: **PASS_WITH_WARNINGS**
   - `final < 70` OR `critical_count > 0`: **FAIL**

### Phase 4: Export and Display

1. **Construct export JSON payload** with all synthesized data (see schema below)
2. **Write to temp file**: `/tmp/code_review_export.json`
3. **Run export script**:

```bash
~/.claude/scripts/.venv/bin/python3 \
  ~/.claude/plugins/marketplaces/rok-plugin-marketplace/production-code-review/scripts/code_review_export.py \
  --input /tmp/code_review_export.json
```

4. **Clean up**: `rm /tmp/code_review_export.json`
5. **Display summary in chat**:

```
## Production Code Review Complete

**Project**: [name]
**Verdict**: PASS / PASS_WITH_WARNINGS / FAIL
**Production Readiness Score**: 78/100

| Dimension       | Score | Issues |
|-----------------|-------|--------|
| Code Quality    | 82    | 3      |
| Testing         | 65    | 7      |
| UI/UX           | 88    | 2      |
| Responsive      | 75    | 4      |
| Security        | 90    | 1      |
| Performance     | 72    | 3      |

**Critical**: 0  |  **High**: 5  |  **Medium**: 8  |  **Low**: 7

### Top Issues
1. [SEC-001] SQL injection in user endpoint - src/api/users.ts:42
2. [TEST-003] No tests for auth middleware - src/middleware/auth.ts
3. [RD-002] Table overflows on mobile - src/components/Dashboard.tsx:67

### Exports
- Markdown: [path]
- PDF: [path]
- HTML: [path]
```

## Export JSON Schema

```json
{
  "type": "code_review",
  "project_name": "...",
  "project_path": "/path/to/project",
  "date": "YYYY-MM-DD",
  "verdict": "PASS|PASS_WITH_WARNINGS|FAIL",
  "production_readiness_score": 78,
  "dimensions": [
    {
      "name": "Code Quality",
      "key": "code_quality",
      "score": 82,
      "weight": 0.20,
      "issue_count": 3,
      "summary": "...",
      "positive_findings": ["..."]
    }
  ],
  "issues": [
    {
      "id": "SEC-001",
      "dimension": "security",
      "severity": "CRITICAL",
      "confidence": 95,
      "title": "...",
      "description": "...",
      "files": [{"path": "...", "line": 42}],
      "recommendation": "...",
      "category": "..."
    }
  ],
  "issue_summary": {
    "critical": 0,
    "high": 5,
    "medium": 8,
    "low": 7,
    "total": 20
  },
  "executive_summary": "2-3 sentence overall assessment",
  "recommendations": ["...", "..."],
  "tech_stack": "Next.js 14, React 18, Tailwind CSS",
  "files_reviewed_total": 147
}
```

## Error Handling

- **Agent timeout**: Log partial results, note incomplete coverage for that dimension
- **Agent failure**: Continue with remaining agents, default missing dimension to score 50
- **Export script failure**: Display full report in chat as fallback, retry export
- **No source files**: Inform user and exit early
- **Non-web project**: Skip UI/UX and responsive dimensions, adjust weights proportionally

## Token Budget

| Phase | Estimated Cost |
|-------|---------------|
| Phase 1 (scan) | ~2K tokens |
| Phase 2 (6 agents) | ~60-90K tokens |
| Phase 3 (synthesis) | ~5K tokens |
| Phase 4 (export) | ~2K tokens |
| **Total** | **~70-100K tokens** |

## Notes

- This is a READ-ONLY review. No files are modified.
- Use TodoWrite to track progress through all 4 phases.
- All issues must include specific file paths and line numbers.
- The confidence >= 80 threshold prevents false positives.
- The export goes to: `C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\Code_Reviews\`
