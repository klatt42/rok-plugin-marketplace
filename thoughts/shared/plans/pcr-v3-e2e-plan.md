# Implementation Plan: Production Code Review v3.0 - E2E Validation Dimension

**Date**: 2026-02-26
**Planner**: Claude Opus 4.6
**Research source**: thoughts/shared/research/pcr-v3-e2e-research.md
**Protocol**: Full Feynman Pre-Implementation
**Status**: IMPLEMENTED (2026-02-26)

## Pre-Implementation Protocol Summary

### Essential Puzzle Reduction

Our code review plugin reads source code to find bugs but never actually runs the app to see if it works. We want to add a step that launches the app in a browser, clicks through user flows, and reports what's broken. The core puzzle is fitting an async, stateful, file-producing browser testing process into a pipeline designed for stateless JSON-in/JSON-out agents.

### Approaches Considered

| Approach | Description | Selected? |
|----------|-------------|-----------|
| A - Static E2E Only | Analyze E2E test files statically | No - overlaps with testing dimension, doesn't deliver live validation |
| B - Cole Verbatim | Full live E2E with self-healing | No - breaks read-only contract, sequential=slow, Claude-only |
| **C - Hybrid Fan-Out** | **Auto-generate YAML stories, fan-out browser-qa agents in parallel** | **YES** |
| D - Manual YAML Only | Rely on pre-existing YAML stories | No - requires manual story creation per project |

### Key Assumptions Verified

| Assumption | Status | Evidence |
|------------|--------|----------|
| DIMENSION_NAMES supports new entries | Verified | Line 59-66 of code_review_export.py |
| browser-qa accepts auto-generated YAML | Verified | browser-qa.md accepts steps list |
| playwright-cli headless in WSL2 | Verified | SKILL.md confirms |
| fpdf2 can embed images from paths | Verified | pdf.image(filename, x, y, w, h) |
| Screenshots persist after agent completes | Verified | ./ai_review/screenshots/<story>/ |

---

## Selected Approach

**Name**: Hybrid Browser-QA Fan-Out with Auto-Generated Stories

**Summary**: Add E2E as an optional 7th review dimension. A research sub-agent discovers app structure and auto-generates YAML user stories. Browser-qa agents execute stories in parallel via playwright-cli. Results are scored as pass/fail per journey, aggregated into the E2E dimension score, and merged into the unified report with screenshot file references.

## Prerequisites

- [ ] agent-browser or playwright-cli installed globally (`npm install -g agent-browser @playwright/cli`)
- [ ] Project has a browser-accessible frontend
- [ ] Dev server can be started via `npm run dev` or similar

## Step-by-Step Implementation

### Step 1: Create E2E Validator Agent Definition

**Files affected**:
- NEW: `production-code-review/agents/e2e-validator.md`

**Changes**:
Create agent definition with:
- model: sonnet (research phase) + dispatches browser-qa sub-agents
- Pre-flight checks: platform (Linux/WSL/macOS), frontend detection, playwright-cli installation
- Phase A: Research sub-agent discovers app structure, routes, user journeys, DB schema, dev server command
- Phase B: Generate YAML stories from research (one per user journey, using template patterns from our existing templates)
- Phase C: Start dev server in background, wait for ready
- Phase D: Dispatch browser-qa agents in parallel (one per story) using playwright-cli
- Phase E: Collect results, aggregate pass/fail, take responsive screenshots at 3 viewports
- Phase F: Stop server, return structured JSON

Output JSON schema:
```json
{
  "dimension": "e2e_validation",
  "score": 0-100,
  "issues": [{ id, severity, confidence, title, description, files, recommendation, screenshot_path }],
  "summary": "...",
  "positive_findings": [],
  "journey_results": [
    { "name": "...", "status": "PASS|FAIL|PARTIAL", "steps_total": N, "steps_passed": N, "screenshot_dir": "..." }
  ],
  "screenshot_dir": "e2e-screenshots/",
  "responsive_check": { "mobile": "PASS|FAIL", "tablet": "PASS|FAIL", "desktop": "PASS|FAIL" },
  "files_reviewed": 0,
  "server_startup": { "command": "...", "port": N, "startup_time_ms": N }
}
```

Scoring methodology:
- Start at 100
- Each FAILED journey: -15 (critical path) or -8 (secondary path)
- Each PARTIAL journey: -5
- Missing responsive support (any viewport fails): -10
- Console errors found: -3 per unique error
- DB validation failures: -10 per mismatch
- Floor at 0

**Verification**: Agent definition follows same structure as security-reviewer.md and other existing agents.

**Rollback**: Delete the single file.

---

### Step 2: Create E2E Story Generator Prompt

**Files affected**:
- NEW: `production-code-review/agents/e2e-story-generator.md`

**Changes**:
Create a lightweight sub-agent (model: haiku for speed) that:
1. Reads app structure (routes, components, pages)
2. Reads DB schema if present
3. Identifies user journeys (signup, login, CRUD flows, settings, etc.)
4. Generates YAML stories following our existing format:

```yaml
name: [Journey Name]
url: http://localhost:[port]/[path]
browser: playwright-cli
headed: false
steps:
  - Navigate to [page]
  - Confirm [element] is visible
  - [interaction step]
  - Verify [expected outcome]
  - Check for console errors
```

5. Classifies each journey as "critical" (auth, payment, core CRUD) or "secondary" (settings, profile, about)
6. Returns array of story objects + dev server startup command

**Verification**: Generate stories for a known project and validate YAML syntax.

**Rollback**: Delete the single file.

---

### Step 3: Update Review SKILL.md (Entry Point)

**Files affected**:
- EDIT: `production-code-review/skills/review/SKILL.md`

**Changes**:
- Add `e2e_validation` to the triggers list
- Update description to mention 7 dimensions (was 6)
- Add `--skip-e2e` flag documentation (E2E is opt-in for v3.0 initial release)
- Add `--e2e` flag to explicitly include E2E

Note: E2E defaults to OFF because it requires a running server and adds significant time. Users opt in with `--e2e` or `--include=e2e_validation`.

**Verification**: Skill loads correctly, new flags documented.

**Rollback**: Revert edits.

---

### Step 4: Update Review Command (Orchestration Logic)

**Files affected**:
- EDIT: `production-code-review/commands/review.md` (or wherever the orchestration logic lives -- research found the command is defined in the skill/command pattern)

**Changes**:
Add to the dimension dispatch table:
```
{
  "name": "E2E Validation",
  "key": "e2e_validation",
  "agent": "e2e-validator",
  "model": "sonnet",
  "default": false,        # Opt-in
  "requires_frontend": true,
  "flag": "--e2e"
}
```

Phase 2 dispatch logic update:
- If `--e2e` flag present OR `--include` contains `e2e_validation`:
  1. Launch e2e-validator agent via Task (run_in_background: true)
  2. E2E agent runs in parallel with static agents
  3. E2E agent handles its own server startup/shutdown internally
- Otherwise: skip E2E dimension entirely

Phase 3 collection update:
- Collect e2e-validator output via TaskOutput (block: true)
- Parse JSON, handle timeout (default score 50)
- Extract `journey_results` and `screenshot_dir` for report
- Include in scoring only if E2E was run

Weight rebalancing when E2E is included:
```
code_quality:      0.15  (was 0.20)
testing:           0.15  (was 0.20)
security:          0.20  (unchanged)
ui_ux:             0.10  (was 0.15)
responsive_design: 0.10  (was 0.15)
performance:       0.10  (unchanged)
e2e_validation:    0.20  (new)
```

When E2E is NOT included, weights stay at v2.0 values (backward compatible).

**Verification**: Run review with and without `--e2e` flag, verify correct dispatch.

**Rollback**: Revert edits to command file.

---

### Step 5: Update Report Generator Agent

**Files affected**:
- EDIT: `production-code-review/agents/report-generator.md`

**Changes**:
1. Update Step 3 scoring formula to handle 7 dimensions with normalization:
   ```
   if "e2e_validation" in results:
       weights = { code_quality: 0.15, testing: 0.15, security: 0.20,
                   ui_ux: 0.10, responsive_design: 0.10, performance: 0.10,
                   e2e_validation: 0.20 }
   else:
       weights = { code_quality: 0.20, testing: 0.20, security: 0.20,
                   ui_ux: 0.15, responsive_design: 0.15, performance: 0.10 }
   ```

2. Add E2E-specific fields to export JSON schema:
   - `journey_results` array in the E2E dimension object
   - `screenshot_dir` path for report to reference
   - `e2e_screenshots` array: `[{ journey, step, path }]`

3. Update display tables to include E2E row when present

**Verification**: Generate report with and without E2E, verify both formats correct.

**Rollback**: Revert edits.

---

### Step 6: Update Export Script (code_review_export.py)

**Files affected**:
- EDIT: `production-code-review/scripts/code_review_export.py`

**Changes**:

1. **Line 59-66**: Add to DIMENSION_NAMES:
   ```python
   "e2e_validation": "E2E Validation",
   ```

2. **HTML generation**: Add E2E journey results section after score breakdown table:
   ```html
   <!-- E2E Journey Results (only if e2e_validation dimension present) -->
   <h3>E2E Journey Results</h3>
   <table>
     <tr><th>Journey</th><th>Status</th><th>Steps</th><th>Screenshots</th></tr>
     <!-- Per journey: name, PASS/FAIL badge, X/Y steps, link to screenshot dir -->
   </table>
   ```

3. **HTML generation**: For E2E issues with `screenshot_path`, add thumbnail:
   ```html
   <tr><td colspan="...">
     <img src="file:///{screenshot_path}" style="max-width:600px;border:1px solid #E2E8F0;margin:8px 0;">
   </td></tr>
   ```
   Note: HTML uses file:// protocol for local screenshots. For sharing, screenshots should be in the same output directory.

4. **PDF generation**: After E2E issue recommendation rows, embed screenshot:
   ```python
   if iss.get("screenshot_path") and os.path.exists(iss["screenshot_path"]):
       try:
           pdf.image(iss["screenshot_path"], x=pdf.l_margin, w=150)
           pdf.ln(5)
       except Exception:
           pass  # Skip if image can't be embedded
   ```

5. **Markdown generation**: Reference screenshots with relative paths:
   ```markdown
   ![E2E Screenshot](./e2e-screenshots/journey-name/03-step.png)
   ```

6. **Copy screenshots**: After generating reports, copy `e2e-screenshots/` folder to the output directory alongside the MD/PDF/HTML files.

**Verification**: Generate full report with E2E data including screenshots. Open HTML in browser, verify images render. Open PDF, verify images embedded.

**Rollback**: Revert edits to export script.

---

### Step 7: Update Plugin Manifest

**Files affected**:
- EDIT: `production-code-review/.claude-plugin/plugin.json`

**Changes**:
- Bump version from `2.0.0` to `3.0.0`
- Update description to mention E2E validation capability

**Verification**: `python3 tests/validate_plugins.py` passes.

**Rollback**: Revert version bump.

---

### Step 8: Update Code Review Methodology Skill

**Files affected**:
- EDIT: `production-code-review/skills/code-review-methodology/SKILL.md`

**Changes**:
- Add E2E Validation scoring methodology
- Update weight tables (both with-E2E and without-E2E variants)
- Add E2E-specific severity classifications:
  - CRITICAL: Core user journey completely blocked (signup, login, checkout)
  - HIGH: Secondary journey fails or DB validation mismatch
  - MEDIUM: Partial journey failure, cosmetic UI issues in flow
  - LOW: Console warnings, minor viewport issues

**Verification**: Read methodology, confirm scoring criteria are clear.

**Rollback**: Revert edits.

---

## Testing Plan

### Unit Tests
- [ ] E2E story generator produces valid YAML for a Next.js + Supabase project
- [ ] E2E story generator produces valid YAML for a Vite + SQLite project
- [ ] E2E validator agent handles "no frontend" gracefully (skips with score N/A)
- [ ] E2E validator agent handles server startup failure gracefully
- [ ] Export script renders E2E dimension in HTML without errors
- [ ] Export script handles missing screenshot files without crashing

### Integration Tests
- [ ] Full review with `--e2e` on tit-trainer-web (Next.js 16, Supabase, port 4200)
- [ ] Full review without `--e2e` produces identical v2.0 output (backward compatible)
- [ ] Full review with `--include=e2e_validation` runs ONLY E2E dimension
- [ ] Multi-model review with `--e2e --mode=multi` (Claude does live E2E, Codex/Gemini skip E2E)

### Manual Verification
1. Run `/production-code-review:review --e2e` on a project with frontend
2. Verify E2E dimension appears in score breakdown
3. Open HTML report, confirm journey results table renders
4. Confirm screenshot thumbnails display in HTML
5. Open PDF, confirm screenshots are embedded
6. Run without `--e2e`, confirm v2.0 behavior unchanged
7. Run `--include=security,e2e_validation` to confirm partial dimension selection works

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| YAML story generation is unreliable | Medium | High | Use templates + validation step; fallback to basic navigation-only stories |
| Dev server fails to start | Medium | Medium | Graceful skip: E2E score = N/A, not included in weighted total |
| Browser-qa agents timeout | Low | Medium | 120s timeout per story; partial results still count |
| Screenshots bloat output directory | Low | Low | Cap at 50 screenshots; cleanup after report generation |
| Multi-model confusion (Codex/Gemini can't do live E2E) | Low | Low | E2E dimension only dispatched to Claude; skipped for external CLIs |

## Definition of Done

- [ ] `e2e-validator.md` agent created and follows existing agent patterns
- [ ] `e2e-story-generator.md` sub-agent created
- [ ] Review skill updated with `--e2e` flag
- [ ] Report generator handles 7 dimensions with correct weight normalization
- [ ] Export script renders E2E in HTML, PDF, and MD with screenshots
- [ ] Plugin version bumped to 3.0.0
- [ ] Methodology skill documents E2E scoring
- [ ] `python3 tests/validate_plugins.py` passes
- [ ] Backward compatibility: review without `--e2e` produces identical v2.0 output
- [ ] At least one successful end-to-end test on a real project

---

**REQUIRES HUMAN APPROVAL BEFORE IMPLEMENTATION**
