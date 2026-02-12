---
description: Comprehensive pre-production code review with single or multi-model (Claude + Codex + Gemini) parallel analysis
argument-hint: [path/to/project] [--mode=single|multi] [--model=claude|codex|gemini] [--scope=full|focused] [--include=dimensions]
allowed-tools: Bash(git:*), Bash(npm:*), Bash(npx:*), Bash(find:*), Bash(wc:*), Bash(ls:*), Bash(python3:*), Bash(codex:*), Bash(gemini:*), Bash(timeout:*), Bash(which:*), Read, Glob, Grep, Write, Task, TaskOutput, TodoWrite
---

# Production Code Review

Run a comprehensive, multi-dimensional code review before deploying to production (Netlify/Vercel). This is NOT a PR review -- it reviews the entire repository for production readiness. Supports single-model (Claude, Codex, or Gemini) or multi-model (all 3 in parallel) review modes.

## Usage

```
/production-code-review:review                              # Full review of cwd (single/claude)
/production-code-review:review /path/to/project             # Specific project
/production-code-review:review --scope=focused src/         # Focus on src/ only
/production-code-review:review --include=security,tests     # Only specific dimensions
/production-code-review:review --mode=multi                 # Multi-model: Claude + Codex + Gemini
/production-code-review:review --mode=single --model=codex  # Single-model: Codex only
/production-code-review:review --mode=single --model=gemini # Single-model: Gemini only
```

## Arguments

- **path** (optional): Project directory. Default: current working directory.
- **--scope** (optional): `full` (default) or `focused` (only specified subdirectory).
- **--include** (optional): Comma-separated dimensions to run. Default: all. Options: `quality`, `tests`, `ui`, `responsive`, `security`, `performance`.
- **--mode** (optional): `single` (default) or `multi`. Single uses one model; multi uses all 3 in parallel.
- **--model** (optional): `claude` (default), `codex`, or `gemini`. Only applies in single mode.

Initial request: $ARGUMENTS

## Workflow

### Phase 0: Mode Selection and CLI Availability

Before anything else, determine the review mode:

1. **Check CLI availability**:
   - Run `which codex` to check if Codex CLI is installed
   - Run `which gemini` to check if Gemini CLI is installed
   - Record availability: `codex_available: true|false`, `gemini_available: true|false`

2. **Determine mode from arguments**:
   - If `--mode=multi` was specified: use multi-model mode (if external CLIs are available)
   - If `--mode=single --model=codex` was specified: use single/codex mode
   - If `--mode=single --model=gemini` was specified: use single/gemini mode
   - If `--mode=single --model=claude` or `--mode=single` was specified: use single/claude mode
   - If no `--mode` specified: present the user with a choice

3. **Interactive mode selection** (only if `--mode` not specified):

   Display to the user:
   ```
   ## Review Mode Selection

   Available models:
   1. [Single] Claude (default)
   2. [Single] Codex   {AVAILABLE | NOT INSTALLED}
   3. [Single] Gemini  {AVAILABLE | NOT INSTALLED}
   4. [Multi]  All available models in parallel

   Press Enter for default (single/claude), or select 1-4:
   ```

   - Default (Enter) = single/claude (fully backward compatible)
   - If user selects an unavailable external CLI, warn and fall back to single/claude

4. **Validate selection**:
   - If mode=single, model=codex but `codex_available=false`: warn user, fall back to single/claude
   - If mode=single, model=gemini but `gemini_available=false`: warn user, fall back to single/claude
   - If mode=multi: disable any unavailable external CLIs, warn user. If NEITHER external CLI is available, fall back to single/claude with a note.

5. **Record final configuration**:
   ```
   REVIEW MODE: single|multi
   MODEL(S): claude | codex | gemini | claude+codex+gemini | claude+codex | claude+gemini
   ```

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

### Phase 2: Dispatch Reviews (Branching by Mode)

Determine which of the 6 dimensions to launch based on the `--include` flag (default: all):

1. **code-quality-reviewer** (key: `code_quality`) - DRY, SOLID, naming, structure, dead code
2. **test-coverage-reviewer** (key: `testing`) - Coverage gaps, test quality, E2E
3. **ui-ux-reviewer** (key: `ui_ux`) - Contrast, fonts, images, accessibility
4. **responsive-design-reviewer** (key: `responsive_design`) - Breakpoints, mobile, touch targets
5. **security-reviewer** (key: `security`) - OWASP Top 10, secrets, injection
6. **performance-reviewer** (key: `performance`) - Bundle size, N+1, memory leaks

For each dimension, read the corresponding agent definition from:
`~/.claude/plugins/marketplaces/rok-plugin-marketplace/production-code-review/agents/{agent-name}.md`

Extract the Review Checklist and Output Format sections to build prompts for external CLIs.

---

#### Mode: single/claude

Existing behavior. Launch all applicable review agents simultaneously using `Task` with `run_in_background: true`. Each agent receives the Project Context Brief plus its dimension-specific instructions. **All agents should be dispatched in a single message for maximum parallelism.**

Each agent prompt should include:
- The Project Context Brief from Phase 1
- The agent's specific review instructions (from its agent definition file)
- The project path to review
- Instruction to return ONLY structured JSON in the required output format

Use `subagent_type: "general-purpose"` for all agents, embedding the agent's review instructions in the prompt.

Agent model assignments:
- **code-quality-reviewer**: Opus
- **test-coverage-reviewer**: Sonnet
- **ui-ux-reviewer**: Sonnet
- **responsive-design-reviewer**: Sonnet
- **security-reviewer**: Opus
- **performance-reviewer**: Sonnet

---

#### Mode: single/codex

For each applicable dimension, run a background Bash command:

```bash
timeout 300 codex exec \
  -C {project_path} \
  -s read-only \
  -m "gpt-5.3-codex" \
  --ephemeral \
  --color never \
  --output-schema ~/.claude/plugins/marketplaces/rok-plugin-marketplace/production-code-review/scripts/review_output_schema.json \
  -o /tmp/codex_review_{dimension_key}.json \
  "{prompt}"
```

The `{prompt}` for each dimension must include:
1. The Project Context Brief from Phase 1
2. The dimension-specific review checklist (extracted from the agent .md file)
3. JSON output instructions requiring the standard schema (dimension key, score, issues array, summary, positive_findings)

All 6 Bash commands should be dispatched with `run_in_background: true` for maximum parallelism.

---

#### Mode: single/gemini

For each applicable dimension, run a background Bash command:

```bash
timeout 300 gemini \
  -p "{prompt}" \
  -m "gemini-2.5-pro" \
  -o json \
  --approval-mode plan \
  --include-directories {project_path} \
  > /tmp/gemini_review_{dimension_key}.json 2>/dev/null
```

The `{prompt}` for each dimension must include:
1. The Project Context Brief from Phase 1
2. The dimension-specific review checklist (extracted from the agent .md file)
3. JSON output instructions requiring the standard schema (dimension key, score, issues array, summary, positive_findings)

All 6 Bash commands should be dispatched with `run_in_background: true` for maximum parallelism.

---

#### Mode: multi

Dispatch ALL available models simultaneously. For each applicable dimension, launch up to 3 parallel reviews:

- **Claude**: Task subagent with `run_in_background: true` (same as single/claude)
- **Codex**: Background Bash command (same as single/codex), if codex_available
- **Gemini**: Background Bash command (same as single/gemini), if gemini_available

This means up to 18 parallel review tasks (6 dimensions x 3 models). All should be dispatched in a single message for maximum parallelism.

### Phase 3: Collect and Synthesize Results

Collection and synthesis differ by mode:

---

#### Single/claude Collection

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

---

#### Single/codex or Single/gemini Collection

1. **Read output files**: For each dimension, read `/tmp/{model}_review_{dimension_key}.json`
2. **Parse JSON**: The file should contain the standard review schema. Handle these cases:
   - Valid JSON: parse directly
   - JSON wrapped in markdown code blocks (````json ... ````): extract JSON content via regex
   - Invalid/empty output: treat as failure, assign default score 50 with 0 issues
3. **Handle failures**: If a file is missing or unparseable after retries, note as "incomplete" with score 50
4. **Filter issues**: Only include issues with `confidence >= 80`
5. **Deduplicate**: If multiple dimensions flag the same file:line, merge findings
6. **Calculate Production Readiness Score**: Same formula as single/claude (see above)
7. **Determine Verdict**: Same rules as single/claude (see above)
8. **Clean up temp files**: Remove `/tmp/{model}_review_*.json`

---

#### Multi-model Collection and Synthesis

**Phase 3A: Collect from all models**

1. **Claude results**: Collect via `TaskOutput` with `block: true` for each Claude subagent
2. **Codex results**: Read each `/tmp/codex_review_{dimension_key}.json` file. Parse JSON (handle code blocks, fallback to score 50 on failure).
3. **Gemini results**: Read each `/tmp/gemini_review_{dimension_key}.json` file. Parse JSON (handle code blocks, fallback to score 50 on failure).
4. Build a combined results object:
   ```json
   {
     "models": {
       "claude": { "code_quality": {...}, "testing": {...}, ... },
       "codex": { "code_quality": {...}, "testing": {...}, ... },
       "gemini": { "code_quality": {...}, "testing": {...}, ... }
     },
     "project_context": {
       "project_name": "...",
       "project_path": "...",
       "tech_stack": "...",
       "files_reviewed_total": 147
     }
   }
   ```

**Phase 3B: Dispatch multi-model synthesizer**

1. Write the combined results object to `/tmp/multi_model_review_input.json`
2. Dispatch the **multi-model-synthesizer** agent (defined in `agents/multi-model-synthesizer.md`) via `Task`:
   - Pass the combined results as the prompt payload
   - The synthesizer merges findings, deduplicates by file:line proximity, applies consensus scoring, and returns the unified payload
3. Collect the synthesizer output via `TaskOutput` with `block: true`
4. Parse the unified payload -- this becomes the final review result
5. **Clean up temp files**: Remove `/tmp/codex_review_*.json`, `/tmp/gemini_review_*.json`, `/tmp/multi_model_review_input.json`

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
5. **Display summary in chat** (format depends on mode):

---

#### Single-model Display

```
## Production Code Review Complete

**Project**: [name]
**Verdict**: PASS / PASS_WITH_WARNINGS / FAIL
**Production Readiness Score**: 78/100
**Model**: Claude / Codex / Gemini

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

---

#### Multi-model Display

```
## Multi-Model Production Code Review Complete

**Project**: [name]
**Verdict**: PASS / PASS_WITH_WARNINGS / FAIL
**Production Readiness Score**: 78/100
**Models Used**: Claude, Codex, Gemini

| Dimension       | Claude | Codex | Gemini | Consensus | Issues |
|-----------------|--------|-------|--------|-----------|--------|
| Code Quality    | 82     | 78    | 80     | 80        | 5      |
| Testing         | 65     | 70    | 68     | 68        | 7      |
| UI/UX           | 88     | 85    | 90     | 88        | 2      |
| Responsive      | 75     | 72    | 78     | 75        | 4      |
| Security        | 90     | 88    | 92     | 90        | 1      |
| Performance     | 72     | 75    | 70     | 72        | 3      |

**Critical**: 0  |  **High**: 5  |  **Medium**: 8  |  **Low**: 7

### High-Confidence Consensus Findings (2-3 models agree)
1. [SEC-001] SQL injection in user endpoint (3/3 models) - src/api/users.ts:42
2. [TEST-003] No tests for auth middleware (2/3 models) - src/middleware/auth.ts
3. [PERF-002] Unoptimized image loading (3/3 models) - src/components/Hero.tsx:15

### Unique Findings
4. [CQ-005] God component exceeds 500 lines (Claude only) - src/components/Dashboard.tsx
5. [RD-004] Missing touch target sizing (Gemini only) - src/components/Nav.tsx:28

### Model Agreement Summary
- High agreement issues: [count]
- Unique Claude findings: [count]
- Unique Codex findings: [count]
- Unique Gemini findings: [count]

### Exports
- Markdown: [path]
- PDF: [path]
- HTML: [path]
```

## Export JSON Schema

### Single-model Schema

```json
{
  "type": "code_review",
  "review_mode": "single",
  "model_used": "claude|codex|gemini",
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

### Multi-model Schema

```json
{
  "type": "code_review",
  "review_mode": "multi",
  "models_used": ["claude", "codex", "gemini"],
  "project_name": "...",
  "project_path": "/path/to/project",
  "date": "YYYY-MM-DD",
  "verdict": "PASS|PASS_WITH_WARNINGS|FAIL",
  "production_readiness_score": 78,
  "model_scores": {
    "claude": { "code_quality": 82, "testing": 65, "ui_ux": 88, "responsive_design": 75, "security": 90, "performance": 72 },
    "codex": { "code_quality": 78, "testing": 70, "ui_ux": 85, "responsive_design": 72, "security": 88, "performance": 75 },
    "gemini": { "code_quality": 80, "testing": 68, "ui_ux": 90, "responsive_design": 78, "security": 92, "performance": 70 }
  },
  "dimensions": [
    {
      "name": "Code Quality",
      "key": "code_quality",
      "score": 80,
      "weight": 0.20,
      "issue_count": 5,
      "summary": "...",
      "positive_findings": ["..."],
      "model_disagreement": false
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
      "category": "...",
      "source_models": ["claude", "codex", "gemini"],
      "model_agreement": 3
    }
  ],
  "issue_summary": {
    "critical": 0,
    "high": 5,
    "medium": 8,
    "low": 7,
    "total": 20
  },
  "consensus_analysis": {
    "high_agreement_issues": 12,
    "unique_claude_findings": 3,
    "unique_codex_findings": 2,
    "unique_gemini_findings": 4,
    "dimension_disagreements": [],
    "strongest_consensus": "..."
  },
  "executive_summary": "2-3 sentence overall assessment including model agreement notes",
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
- **Codex CLI not found** (`which codex` fails): Disable Codex model, warn user with install instructions
- **Gemini CLI not found** (`which gemini` fails): Disable Gemini model, warn user with install instructions
- **CLI authentication failure**: Warn user with the appropriate auth command (`codex auth` or `gemini auth`), fall back to single/claude
- **CLI output not valid JSON**: Attempt regex extraction of JSON from code blocks (````json...````). If that fails, assign fallback score 50 with 0 issues for that dimension.
- **All external CLIs fail in multi-mode**: Degrade gracefully to single/claude, inform user that external models were unavailable and review continues with Claude only

## Token Budget

| Phase | Single (Claude) | Single (Codex/Gemini) | Multi-Model |
|-------|------------------|-----------------------|-------------|
| Phase 0 (mode select) | ~0.5K | ~0.5K | ~0.5K |
| Phase 1 (scan) | ~2K | ~2K | ~2K |
| Phase 2 (dispatch) | ~60-90K | ~1K (prompts only) | ~60-90K (Claude) + external |
| Phase 3 (synthesis) | ~5K | ~5K | ~15K (with synthesis agent) |
| Phase 4 (export) | ~2K | ~2K | ~2K |
| **Total** | **~70-100K** | **~10-12K** + external | **~80-110K** + external |

Note: Codex and Gemini token costs are on their respective API accounts, not the Claude context window.

## Notes

- This is a READ-ONLY review. No files are modified.
- Use TodoWrite to track progress through all 5 phases (0-4).
- All issues must include specific file paths and line numbers.
- The confidence >= 80 threshold prevents false positives.
- The export goes to: `C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\Code_Reviews\`
- Multi-model mode dispatches reviews to Claude, Codex CLI, and Gemini CLI in parallel for cross-model validation.
- External CLI costs (Codex, Gemini) are billed to their respective API accounts, not to the Claude context budget.
- Single/claude mode is identical to v1.0 behavior -- full backward compatibility is preserved.
- In multi-model mode, consensus findings (2-3 models agree) have boosted confidence and are prioritized in recommendations.
- The multi-model-synthesizer agent handles all cross-model merging, deduplication, and consensus scoring.
