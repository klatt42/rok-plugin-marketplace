---
name: gemini-adapter
description: |
  Reference document for invoking Google Gemini CLI to perform code review
  for a specific dimension. Defines command construction, output parsing,
  and error handling. Read by the orchestrating review command to know
  the exact invocation pattern for non-interactive Gemini review.
---

# Gemini CLI Adapter

## CLI Version

Gemini CLI v0.28.2+

## Invocation Pattern

For each review dimension, construct and run:

```bash
timeout 300 gemini \
  -p "{review_prompt}" \
  -m "gemini-2.5-pro" \
  --approval-mode yolo \
  --include-directories {project_path} \
  > /tmp/gemini_review_{dimension}.txt 2>/tmp/gemini_review_{dimension}.err
```

### Flags Explained

| Flag | Purpose |
|------|---------|
| `-p "{prompt}"` | Non-interactive (headless) mode with the given prompt |
| `-m "gemini-2.5-pro"` | Model selection |
| `--approval-mode yolo` | Auto-approve all tool calls (read-only by prompt instruction). NOTE: `plan` mode requires `experimental.plan` in settings -- use `yolo` for compatibility |
| `--include-directories` | Additional directories to include in workspace |

### Important Notes

- Do NOT use `-o json` -- it wraps the entire session in metadata JSON (stats, tool calls), NOT the model's response. Instead, capture text output and extract JSON from it.
- Do NOT use `2>/dev/null` -- capture stderr to `/tmp/gemini_review_{dimension}.err` for debugging failures.
- The `--approval-mode plan` flag requires `experimental.plan` to be enabled in `~/.gemini/settings.json`. Use `yolo` instead, which works without experimental flags. The prompt already instructs Gemini not to modify files.

## Prompt Construction

The review prompt must include three sections:

```
You are reviewing a codebase for production readiness, focusing on {DIMENSION_NAME}.

PROJECT CONTEXT
===============
{project_context_brief}

REVIEW CHECKLIST
================
{dimension_review_checklist_from_agent_md}

CRITICAL OUTPUT REQUIREMENTS
============================
Your ENTIRE response must be ONLY valid JSON. No markdown. No code blocks.
No preamble. No explanation. Just a single JSON object.

Required fields:
- dimension: "{dimension_key}" (string)
- score: 0-100 (integer)
- issues: array of objects, each with:
  - id: "{PREFIX}-{NNN}" (string)
  - severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
  - confidence: 0-100 (integer)
  - title: brief issue title (string)
  - description: detailed explanation (string)
  - files: array of {path, line} objects
  - recommendation: how to fix (string)
  - category: issue category (string)
- summary: brief assessment (string)
- positive_findings: array of strings
- files_reviewed: integer count

Begin your review now.
```

## Dimension Keys

| Dimension | Key | ID Prefix |
|-----------|-----|-----------|
| Code Quality | code_quality | CQ |
| Testing | testing | TEST |
| UI/UX | ui_ux | UI |
| Responsive Design | responsive_design | RD |
| Security | security | SEC |
| Performance | performance | PERF |

## Output Parsing

Gemini outputs text that contains the model's response (which should be JSON per the prompt). Parse strategy:

1. Read file content from `/tmp/gemini_review_{dimension}.txt` with `Read` tool
2. Strip any ANSI escape codes and Gemini CLI status lines (lines starting with "Loaded cached", "Session cleanup", "Hook registry", "YOLO mode")
3. If remaining content is valid JSON, use it directly
4. If content contains a JSON code block (```json ... ```), extract and parse inner content
5. If content is plain text containing a `{...}` object, regex-extract the outermost JSON object
6. If parsing fails, check `/tmp/gemini_review_{dimension}.err` for error details
7. Fallback: return default score-50 result

```json
{
  "dimension": "{dimension_key}",
  "score": 50,
  "issues": [],
  "summary": "Gemini output could not be parsed as JSON",
  "positive_findings": [],
  "files_reviewed": 0
}
```

## Timeout Handling

- Timeout: 300 seconds (5 minutes) per dimension
- If timeout occurs, the output file may be empty or partial
- Record: score 50, issues empty, summary "Gemini review timed out for {dimension}"

## Error Handling

On failure, ALWAYS read the `.err` file first for diagnostics:

| Error | Detection | Response |
|-------|-----------|----------|
| Not installed | `which gemini` returns empty | Skip Gemini, warn user |
| Auth failure | stderr contains "auth" or "credentials" | Warn: "Run `gemini auth login` to authenticate" |
| Plan mode error | stderr contains "experimental.plan" | Already fixed: adapter uses `yolo` mode instead |
| Model unavailable | stderr contains "model" error | Try fallback `-m gemini-2.5-flash` |
| Rate limited | stderr contains "quota" or "429" or "exhausted your capacity" | Wait 10s, retry once, then skip |
| Non-zero exit | Exit code != 0 | Read .err file, log error, use fallback score 50 |

## File Cleanup

After parsing all dimension results, clean up temp files:

```
/tmp/gemini_review_code_quality.txt
/tmp/gemini_review_code_quality.err
/tmp/gemini_review_testing.txt
/tmp/gemini_review_testing.err
/tmp/gemini_review_ui_ux.txt
/tmp/gemini_review_ui_ux.err
/tmp/gemini_review_responsive_design.txt
/tmp/gemini_review_responsive_design.err
/tmp/gemini_review_security.txt
/tmp/gemini_review_security.err
/tmp/gemini_review_performance.txt
/tmp/gemini_review_performance.err
```
