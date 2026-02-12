---
name: codex-adapter
description: |
  Reference document for invoking OpenAI Codex CLI to perform code review
  for a specific dimension. Defines command construction, output parsing,
  and error handling. Read by the orchestrating review command to know
  the exact invocation pattern for non-interactive Codex review.
---

# Codex CLI Adapter

## CLI Version

Codex CLI v0.99.0+ (`@openai/codex`)

## Invocation Pattern

For each review dimension, construct and run:

```bash
timeout 300 codex exec \
  -C {project_path} \
  -s read-only \
  -m "gpt-5.3-codex" \
  --ephemeral \
  --color never \
  --output-schema {plugin_path}/scripts/review_output_schema.json \
  -o /tmp/codex_review_{dimension}.json \
  "{review_prompt}"
```

### Flags Explained

| Flag | Purpose |
|------|---------|
| `-C {project_path}` | Set working directory to the project being reviewed |
| `-s read-only` | Sandbox: no file modifications allowed |
| `-m "gpt-5.3-codex"` | Model selection (default Codex model) |
| `--ephemeral` | No session files persisted to disk |
| `--color never` | Strip ANSI escape codes from output |
| `--output-schema` | JSON Schema file constraining the model's output shape |
| `-o /tmp/codex_review_{dimension}.json` | Write last agent message to this file |

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

OUTPUT REQUIREMENTS
===================
Return ONLY valid JSON matching the output schema. No markdown code blocks.
No preamble. No explanation text. Just the JSON object.

Required fields:
- dimension: "{dimension_key}"
- score: 0-100 integer
- issues: array of issue objects with id, severity, confidence, title, description, files, recommendation
- summary: brief assessment string
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

Codex writes the last agent message to the `-o` file. Parse strategy:

1. Read file content with `Read` tool
2. If content starts with `{` or `[`, parse as JSON directly
3. If content contains a JSON code block (```json ... ```), extract and parse the inner content
4. If content contains a bare `{...}` block, regex-extract first complete JSON object
5. If all parse attempts fail, return fallback:
   ```json
   {
     "dimension": "{dimension_key}",
     "score": 50,
     "issues": [],
     "summary": "Codex output could not be parsed as JSON",
     "positive_findings": [],
     "files_reviewed": 0
   }
   ```

## Timeout Handling

- Timeout: 300 seconds (5 minutes) per dimension
- If timeout occurs, the `-o` file may be empty or partial
- Record: score 50, issues empty, summary "Codex review timed out for {dimension}"

## Error Handling

| Error | Detection | Response |
|-------|-----------|----------|
| Not installed | `which codex` returns empty | Skip Codex, warn user |
| Auth failure | stderr contains "authentication" or "API key" | Warn: "Run `codex login` to authenticate" |
| Model unavailable | stderr contains "model" error | Try fallback model or skip |
| Rate limited | stderr contains "rate" or "429" | Wait 10s, retry once, then skip |
| Non-zero exit | Exit code != 0 | Log error, use fallback score 50 |

## File Cleanup

After parsing all dimension results, clean up temp files:

```
/tmp/codex_review_code_quality.json
/tmp/codex_review_testing.json
/tmp/codex_review_ui_ux.json
/tmp/codex_review_responsive_design.json
/tmp/codex_review_security.json
/tmp/codex_review_performance.json
```
