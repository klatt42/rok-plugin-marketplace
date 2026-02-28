---
description: Deep codebase analysis producing handoff documents for CC sessions with maturity scoring
argument-hint: [path|github-url|user/repo] [--mode=single|suite]
allowed-tools: Bash(git:*), Bash(gh:*), Bash(find:*), Bash(wc:*), Bash(ls:*), Bash(python3:*), Bash(rm:*), Bash(timeout:*), Bash(which:*), Read, Glob, Grep, Write, Task, TaskOutput, TodoWrite
---

# Repo Summarizer

Analyze a repository to produce a comprehensive handoff document for another Claude Code session. Maps purpose, features, tech stack, gaps, and architecture. Calculates a Repo Maturity Score and exports to MD, PDF, and HTML.

## Usage

```
/repo-summarizer:summarize                              # Analyze current directory
/repo-summarizer:summarize /path/to/project             # Local project path
/repo-summarizer:summarize https://github.com/user/repo # Clone from GitHub
/repo-summarizer:summarize user/repo                    # GitHub shorthand
/repo-summarizer:summarize --mode=suite repo1,repo2     # Analyze multiple repos
```

## Arguments

- **source** (optional): Local path, GitHub URL, or user/repo shorthand. Default: current working directory.
- **--mode** (optional): `single` (default) or `suite` (multi-repo analysis with cross-repo integration check).

Initial request: $ARGUMENTS

## Workflow

### Phase 0: Resolve Source

1. **Determine source type**:
   - If no argument or `.` or local path: use as-is (verify directory exists)
   - If GitHub URL (`https://github.com/...`): clone via `gh repo clone` to /tmp/repo-summarizer/{repo-name}
   - If shorthand (`user/repo`): clone via `gh repo clone user/repo` to /tmp/repo-summarizer/{repo-name}
   - For suite mode: parse comma-separated list, resolve each source

2. **Clone if needed**:
   ```bash
   mkdir -p /tmp/repo-summarizer
   gh repo clone {url_or_shorthand} /tmp/repo-summarizer/{repo-name} -- --shallow-since="60 days ago"
   ```
   - Use `--shallow-since="60 days ago"` for recency coverage (deeper than depth=50)
   - If clone fails, check `gh auth status` and report auth issue

3. **Verify source**:
   - Confirm directory exists and contains source files
   - Check for git repo (`.git/` directory)
   - If empty or no source files, abort with message

4. **Record source info**:
   ```
   SOURCE: local | github
   PATH: /absolute/path/to/project
   REPO_URL: https://github.com/user/repo (if applicable)
   CLEANUP: true | false (true if we cloned it)
   ```

For **suite mode**: repeat for each repo. Track list of resolved sources.

### Phase 1: Project Intelligence Scan

Before launching agents, gather project intelligence:

1. **Identify project name**: From package.json `name`, Cargo.toml `[package].name`, directory name
2. **Identify primary language**: Count source files by extension
   ```bash
   find {path} -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.rs" -o -name "*.go" -o -name "*.rb" -o -name "*.java" \) | head -500 | awk -F. '{print $NF}' | sort | uniq -c | sort -rn
   ```
3. **Count source files**: Total files in key directories
4. **Git statistics** (if git repo):
   ```bash
   git -C {path} log --oneline -20
   git -C {path} shortlog -sn --all | head -10
   git -C {path} log --format="%ai" -1
   ```
5. **Identify framework**: Read package.json, pyproject.toml, go.mod first few lines
6. **Check for CLAUDE.md**: Project conventions document
7. **Check for CI/CD**: .github/workflows/, .gitlab-ci.yml
8. **Check for deploy config**: netlify.toml, vercel.json, Dockerfile, fly.toml
9. **Run test suite** (best-effort, not required):
   Detect the test runner:
   - Node.js: `pnpm-lock.yaml` -> `pnpm test`, `package-lock.json` -> `npm test`, `yarn.lock` -> `yarn test`
   - Python: pytest markers/conftest.py -> `python -m pytest --tb=no -q`
   - Rust: `cargo test`
   - Go: `go test ./...`

   Execute with timeout: `timeout 60 {test_command} 2>&1`

   Parse output to extract:
   - `total_tests`, `passed_tests`, `failed_tests`, `skipped_tests`
   - `pass_rate` (0.0 - 1.0)
   - `test_runner` name (jest, vitest, pytest, etc.)
   - `error` (if tests couldn't run at all, e.g., missing deps)

   Also glob for test files: `*.test.*`, `*.spec.*`, `test_*`, `*_test.*`
   Record `test_files_count`.

   If no test script found: `total_tests = 0`
   If runner fails entirely: record error, set `total_tests = -1` as sentinel

10. **Collect git recency data** (if git repo):
    ```bash
    # Files changed in last 30 days with change count
    git -C {path} log --since="30 days ago" --name-only --pretty=format:"" | sort | uniq -c | sort -rn | head -50

    # Total commits in last 30 days
    git -C {path} rev-list --count --since="30 days ago" HEAD

    # Most active directories
    git -C {path} log --since="30 days ago" --name-only --pretty=format:"" | xargs -I{} dirname {} 2>/dev/null | sort | uniq -c | sort -rn | head -20
    ```
    Produce: `recently_active_files` (top 50 with change counts), `recently_active_dirs` (top 20), `total_recent_commits`, `recency_window: "30 days"`

Build a **Project Context Brief**:
```
PROJECT CONTEXT
===============
Name: {project_name}
Path: {absolute_path}
URL: {repo_url or "local"}
Primary Language: {language} ({file_count} files)
Framework: {framework_name} {version}
Total Source Files: {count}
Git: {branch}, {commit_count} commits, last commit {date}
Contributors: {top 3}
CLAUDE.md: {present | absent}
Deploy: {platform or "none detected"}
CI/CD: {present | absent}

TEST SUITE
Runner: {runner or "none detected"}
Total: {N} | Passed: {N} | Failed: {N} | Skipped: {N} | Pass Rate: {N}%
Test Files: {count}
Error: {error or "none"}

GIT RECENCY (last 30 days)
Recent Commits: {N}
Top Active Files: {top 10 with counts}
Top Active Dirs: {top 10 with counts}
```

### Phase 2: Dispatch Analysis Agents

Launch all 5 analysis agents simultaneously using `Task` with `run_in_background: true`. **All agents should be dispatched in a single message for maximum parallelism.**

Each agent receives the Project Context Brief plus the project path to analyze.

Read each agent definition from:
`~/.claude/plugins/marketplaces/rok-plugin-marketplace/repo-summarizer/agents/{agent-name}.md`

Extract the full agent instructions to build prompts.

Agent dispatches:

1. **purpose-analyzer** (model: opus)
   - Prompt: Project Context Brief + purpose analysis instructions + project path
   - subagent_type: "general-purpose"

2. **feature-enumerator** (model: opus)
   - Prompt: Project Context Brief + feature enumeration instructions + project path
   - subagent_type: "general-purpose"

3. **stack-analyzer** (model: sonnet)
   - Prompt: Project Context Brief + stack analysis instructions + project path
   - subagent_type: "general-purpose"

4. **gap-finder** (model: opus)
   - Prompt: Project Context Brief + gap analysis instructions + project path
   - subagent_type: "general-purpose"

5. **architecture-mapper** (model: sonnet)
   - Prompt: Project Context Brief + architecture mapping instructions + project path
   - subagent_type: "general-purpose"

### Phase 2S: Suite Cross-Repo Analysis (Suite Mode Only)

After all per-repo Phase 2-3 cycles complete:

1. Collect all per-repo analysis results
2. Dispatch a cross-repo integration analysis agent that:
   - Compares dependencies across repos (find version mismatches)
   - Matches API endpoints (one repo's exports = another's fetch URLs)
   - Finds shared data models (same entity names across repos)
   - Identifies missing integration glue (e.g., no shared auth, inconsistent error formats)
3. Use the same summary-synthesizer agent with `mode: "suite"` and all per-repo data

### Phase 3: Collect and Synthesize

1. **Collect all results**: Use `TaskOutput` with `block: true` for each agent
2. **Parse JSON outputs**: Extract structured data from each agent response. If an agent wrapped its JSON in markdown code blocks, extract the JSON content.
3. **Handle failures**: If an agent timed out or failed, note as "incomplete" and use defaults
4. **Dispatch summary-synthesizer**: Pass all 5 agent outputs plus project context
   - subagent_type: "general-purpose"
   - model: opus
   - The synthesizer calculates the Repo Maturity Score, builds the Handoff Brief, and triggers the export script
5. **Collect synthesizer result**: Use `TaskOutput` with `block: true`

### Phase 4: Display and Cleanup

1. **Parse export result**: The export script returns JSON with file paths
2. **Clean up cloned repos** (if applicable):
   ```bash
   rm -rf /tmp/repo-summarizer/{repo-name}
   ```
3. **Display summary in chat**:

```
## Repo Summary Complete

**Project**: {name}
**Maturity Level**: MATURE / DEVELOPING / EARLY STAGE / PROTOTYPE
**Maturity Score**: {score}/100
**Type**: {project_type} | **Stack**: {framework} + {database} on {platform}

| Dimension              | Score | Weight |
|------------------------|-------|--------|
| Documentation          | {s}   | 15%    |
| Feature Completeness   | {s}   | 30%    |
| Infrastructure         | {s}   | 20%    |
| Test Presence          | {s}   | 15%    |
| Architecture Clarity   | {s}   | 20%    |

**Features**: {complete}/{total} complete | {partial} partial | {stub} stubs | {planned} planned
**Gaps**: {critical} critical | {high} high | {medium} medium | {low} low

### Top Recommendations
1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}

### Exports
- Markdown: {md_path}
- PDF: {pdf_path}
- HTML: {html_path}
```

For **suite mode**, add after the per-repo summaries:
```
### Suite Integration Analysis
- Shared dependencies: {count}
- Version mismatches: {count}
- API contract matches: {count}
- Integration gaps: {count}

### Cross-Repo Recommendations
1. {cross_repo_recommendation_1}
2. {cross_repo_recommendation_2}
```

## Error Handling

- **Agent timeout**: Log partial results, note incomplete coverage for that dimension
- **Agent failure**: Continue with remaining agents, use default scores for missing dimensions
- **Export script failure**: Display full report in chat as fallback, retry export once
- **Clone failure**: Check `gh auth status`, report authentication issue
- **No source files**: Inform user and exit early
- **gh not installed**: Inform user: "GitHub CLI (gh) is required for remote repos. Install: https://cli.github.com/"
- **Empty repository**: Report as PROTOTYPE with score 0

## Token Budget

| Phase | Estimated Cost |
|-------|---------------|
| Phase 0 (resolve) | ~1K |
| Phase 1 (scan + test + recency) | ~5K |
| Phase 2 (dispatch) | ~80-120K (across 5 agents) |
| Phase 3 (synthesis) | ~10K |
| Phase 4 (export) | ~2K |
| **Total** | **~105-150K** |

Suite mode multiplies Phase 1-2 by number of repos and adds ~15K for cross-repo analysis.

## Notes

- This is a READ-ONLY analysis. No files are modified (except /tmp for export).
- Use TodoWrite to track progress through all phases.
- The export goes to: `C:\Users\RonKlatt_3qsjg34\Desktop\Claude Code Plugin Output\Repo_Summaries\`
- The Handoff Brief is the critical output -- structured for direct consumption by another CC session.
- For private repos, `gh` CLI must be authenticated (`gh auth status` to verify).
- Cloned repos are cleaned up after analysis to avoid disk bloat.
- Suite mode is designed for related repos (e.g., FBM apps) -- not arbitrary collections.
