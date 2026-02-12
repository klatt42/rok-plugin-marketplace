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
  -o json \
  --approval-mode plan \
  --include-directories {project_path} \
  > /tmp/gemini_review_{dimension}.json 2>/dev/null
```

### Flags Explained

| Flag | Purpose |
|------|---------|
| `-p "{prompt}"` | Non-interactive (headless) mode with the given prompt |
| `-m "gemini-2.5-pro"` | Model selection |
| `-o json` | Structured JSON output format |
| `--approval-mode plan` | Read-only mode -- analyzes but does not modify files |
| `--include-directories` | Additional directories to include in workspace |

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

Gemini with `-o json` outputs structured JSON with metadata wrapping. Parse strategy:

1. Read file content with `Read` tool
2. Try parsing as JSON directly -- may be the raw model response
3. If the JSON has a `response` or `text` or `content` field, extract and parse that as the review JSON
4. If the outer JSON has a `candidates` array (Gemini API format), extract `candidates[0].content.parts[0].text` and parse
5. If content contains a JSON code block, extract and parse inner content
6. If content is plain text containing a `{...}` object, regex-extract
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

| Error | Detection | Response |
|-------|-----------|----------|
| Not installed | `which gemini` returns empty | Skip Gemini, warn user |
| Auth failure | stderr contains "auth" or "credentials" | Warn: "Run `gemini auth login` to authenticate" |
| Model unavailable | stderr contains "model" error | Try fallback `-m gemini-2.5-flash` |
| Rate limited | stderr contains "quota" or "429" | Wait 10s, retry once, then skip |
| Non-zero exit | Exit code != 0 | Log error, use fallback score 50 |

## File Cleanup

After parsing all dimension results, clean up temp files:

```
/tmp/gemini_review_code_quality.json
/tmp/gemini_review_testing.json
/tmp/gemini_review_ui_ux.json
/tmp/gemini_review_responsive_design.json
/tmp/gemini_review_security.json
/tmp/gemini_review_performance.json
```
