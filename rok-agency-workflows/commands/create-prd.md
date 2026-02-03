# /create-prd - Generate Product Requirements Document

Synthesizes conversation context into a comprehensive PRD that becomes the project's "north star".

## Usage

```
/create-prd                           # Output to PRD.md
/create-prd output:docs/PRD.md        # Custom output path
/create-prd project:rok-copilot       # Include project context
```

## What This Does

1. **Extracts Requirements** from conversation history
2. **Synthesizes** into structured PRD format
3. **Creates PRD.md** as the project's single source of truth
4. **Generates feature_list.json** from PRD features (optional)

## PRD Structure

Create a well-structured PRD with these sections:

### 1. Executive Summary (Required)
```markdown
## 1. Executive Summary

[2-3 paragraphs covering:]
- Product overview and purpose
- Core value proposition
- MVP goal statement
```

### 2. Mission (Required)
```markdown
## 2. Mission

**Mission Statement:** [One sentence]

### Core Principles
1. **Principle Name** - Brief explanation
2. ...
```

### 3. Target Users (Required)
```markdown
## 3. Target Users

### Primary Persona: [Name]
- **Who:** Description
- **Technical Comfort:** Level
- **Goals:** What they want to achieve
- **Pain Points:** Current frustrations
```

### 4. MVP Scope (Required)
```markdown
## 4. MVP Scope

### In Scope
**Core Functionality**
- [x] Feature description
- [x] Feature description

**Technical**
- [x] Technology choice with rationale

### Out of Scope
- [ ] Deferred feature (reason)
- [ ] Future enhancement
```

### 5. User Stories (Required)
```markdown
## 5. User Stories

1. **As a [user], I want to [action], so that [benefit].**
   - Example: Concrete scenario
```

### 6. Core Architecture (Required)
```markdown
## 6. Core Architecture

### High-Level Design
[Diagram or description]

### Directory Structure
```
project/
├── src/
├── tests/
└── docs/
```

### Key Patterns
- Pattern name: How it's used
```

### 7. Technology Stack (Required)
```markdown
## 7. Technology Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Frontend | Next.js | 14.x | SSR, app router |
| Backend | Python | 3.11+ | FastAPI, async |
| Database | PostgreSQL | 15+ | Supabase hosted |
```

### 8. Success Criteria (Required)
```markdown
## 8. Success Criteria

### MVP Definition of Done
- [ ] Criterion 1
- [ ] Criterion 2

### Quality Indicators
- Performance: Target metrics
- Reliability: Uptime goals
```

### 9. Implementation Phases (Required)
```markdown
## 9. Implementation Phases

### Phase 1: Foundation
**Goal:** Core infrastructure
**Deliverables:**
- [ ] Item 1
- [ ] Item 2
**Validation:** How to verify complete

### Phase 2: MVP Features
...
```

### 10. Risks & Mitigations (Required)
```markdown
## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Description | H/M/L | Strategy |
```

### Optional Sections
- API Specification (if building API)
- Security & Configuration (if auth required)
- Future Considerations
- Appendix

## Process

### Step 1: Extract Requirements
- Review entire conversation history
- Identify explicit requirements
- Note technical constraints
- Capture user goals

### Step 2: Synthesize Information
- Organize into sections above
- Fill reasonable assumptions (mark as [ASSUMPTION])
- Ensure technical feasibility
- Maintain consistency

### Step 3: Write the PRD
- Use clear, professional language
- Include concrete examples
- Use markdown formatting extensively
- Add code snippets where helpful

### Step 4: Quality Checks
- [ ] All required sections present
- [ ] User stories have clear benefits
- [ ] MVP scope is realistic
- [ ] Technology choices justified
- [ ] Phases are actionable
- [ ] Success criteria measurable

## Integration with ROK

### Link to feature_list.json
After creating PRD, optionally generate `feature_list.json`:

```
Based on the PRD, shall I generate feature_list.json for structured tracking?
```

If yes, extract features from "In Scope" section into:
```json
{
  "project": "project-name",
  "prd_version": "1.0",
  "created": "YYYY-MM-DD",
  "features": [
    {
      "id": "feature-id",
      "category": "core|infrastructure|integration",
      "description": "From PRD",
      "validation_steps": ["From user stories"],
      "dependencies": [],
      "priority": 1,
      "status": "todo",
      "prd_section": "4.1"
    }
  ]
}
```

### Session Start Integration
When `/session-start` runs, it should:
1. Check if PRD.md exists
2. If yes, display: "PRD loaded: [mission statement summary]"
3. Ask: "Based on the PRD, what should we build next?"

### Progress Tracking
Link PRD phases to `claude-progress.txt`:
```
[2026-01-08] Session Summary
- PRD Phase: 1 (Foundation)
- Completed: feature-auth-login
- In Progress: feature-auth-oauth
```

## Output Confirmation

After creating PRD:
1. Confirm file path written
2. Summary of sections completed
3. List any [ASSUMPTION] markers
4. Suggest: "Run /generate-feature-list to create structured tracking"

## Style Guidelines

- **Tone:** Professional, clear, action-oriented
- **Format:** Markdown with headers, lists, tables, code blocks
- **Checkboxes:** Use `[x]` for in-scope, `[ ]` for out-of-scope/deferred
- **Specificity:** Concrete examples over abstract descriptions
- **Length:** Comprehensive but scannable (typically 200-500 lines)

## Example PRD Header

```markdown
# [Project Name] - Product Requirements Document

**Version:** 1.0
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Status:** Draft | Review | Approved

---

> "The PRD is the north star for the coding agent." - Cole Medin

---

## 1. Executive Summary
...
```

## Notes

- If critical information missing, ask clarifying questions first
- Adapt section depth to available details
- For technical products, emphasize architecture
- For user-facing products, emphasize user stories
- Mark all assumptions explicitly with [ASSUMPTION]

---

**Based on Cole Medin's PRD-First Development pattern**
*Source: github.com/coleam00/habit-tracker*
