# /diary Command

Capture session learnings before context is lost. This command uses Feynman-enhanced prompts to extract deeper insights than simple session summaries.

**Version**: 3.0 (ROK 3.6-Feynman - Enhanced with Feynman Reflection Prompts)

## Execution Steps

### 1. Gather Session Context
Analyze the current session to identify:
- Tasks attempted and their outcomes
- Decisions made during the session
- Problems encountered and solutions found
- New patterns or approaches discovered

### 2. Standard Captures
Create entries for:

**Accomplishments**
- What was completed this session?
- What progress was made on ongoing work?

**Decisions Made**
- What choices were made?
- What was the rationale?
- What alternatives were considered?

**Problems & Solutions**
- What blockers were encountered?
- How were they resolved?
- What would you do differently?

### 3. Feynman-Enhanced Captures (CRITICAL)

**Assumption Corrections** (Most Important)
For each significant discovery, document:
```
What I thought was true:
[Initial assumption or mental model]

What was actually true:
[Corrected understanding]

How I discovered the gap:
[The moment of realization - error message, test failure, user feedback]
```

**Mental Model Updates**
```
Before this session, my model of [concept/system] was:
[Previous understanding]

Now I understand that:
[Updated, more accurate model]

Key insight:
[One sentence that captures the shift]
```

**Pattern Discoveries**
```
New pattern identified:
[Name and description]

When to apply it:
[Conditions where this pattern is useful]

When NOT to apply it:
[Conditions where this pattern would be harmful]

Example from this session:
[Concrete instance]
```

**Future Session Guidance**
```
If working on similar problems, remember:
[Specific advice for future self/sessions]

Watch out for:
[Pitfalls discovered]

Start by:
[Recommended first steps]
```

### 4. Self-Scoring Rubric

Apply the scoring rubric to the current session:

| Criterion | Description | Anchors |
|-----------|-------------|---------|
| **Completion** | Did the session accomplish stated goals? | 1-3: Major gaps, 4-6: Partial, 7-9: Complete, 10: Exceeded |
| **Quality** | Code/output quality and best practices | 1-3: Bugs/issues, 4-6: Functional, 7-9: Clean, 10: Exemplary |
| **Efficiency** | Was time/tokens used effectively? | 1-3: Wasteful, 4-6: Average, 7-9: Efficient, 10: Optimal |
| **Learning** | Were insights captured for future? | 1-3: None, 4-6: Some, 7-9: Good, 10: Comprehensive |
| **Communication** | Was user interaction clear and helpful? | 1-3: Confusing, 4-6: OK, 7-9: Clear, 10: Excellent |

**Quality Bar**: Average >= 7.0 (triggers reflection if below)

### 5. Output Location

Write diary entry to:
`~/.claude/expertise/[project-name]-diary-[YYYY-MM-DD].md`

If multiple entries same day, append with timestamp header.

### 6. Auto-Ingest to Archon (Phase 3)

After creating diary entry, automatically ingest to Archon knowledge base:

```bash
# Trigger ingestion of new diary entry
python3 ~/.claude/scripts/ingest_expertise.py --file [diary-file-path]
```

This ensures new learnings are immediately searchable via `/search-expertise`.

Output:
```
DIARY ENTRY CREATED
───────────────────
File: ~/.claude/expertise/[project]-diary-[date].md
Archon ingestion: ✅ Complete (or ⚠️ Archon unavailable - manual ingest later)

New learnings are now searchable via /search-expertise
```

### 7. Cross-Reference

After creating entry:
- Check if any learnings should update main expertise file
- Flag significant assumption-corrections for next /reflect cycle
- Note any anti-patterns observed for anti-patterns.md

## Output Format

```markdown
# Diary: [Project Name]
## Session: [YYYY-MM-DD HH:MM]

### Self-Assessment
| Criterion | Score | Evidence |
|-----------|-------|----------|
| Completion | X/10 | <evidence> |
| Quality | X/10 | <evidence> |
| Efficiency | X/10 | <evidence> |
| Learning | X/10 | <evidence> |
| Communication | X/10 | <evidence> |

**Average Score**: X.X/10
**Quality Bar Met**: Yes/No

### Accomplishments
- [item]

### Decisions
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [what] | [why] | [what else] |

### Problems & Solutions
| Problem | Solution | Prevention |
|---------|----------|------------|
| [issue] | [fix] | [how to avoid] |

### Assumption Corrections
#### [Topic]
- **Thought**: [assumption]
- **Reality**: [correction]
- **Discovery**: [how learned]

### Mental Model Updates
#### [Concept]
- **Before**: [old model]
- **After**: [new model]
- **Insight**: [key takeaway]

### Pattern Discoveries
#### [Pattern Name]
- **Apply when**: [conditions]
- **Avoid when**: [conditions]
- **Example**: [from session]

### Future Guidance
- [advice item]

---
*Entry created by /diary command v3.0*
```

## Usage

```
/diary
```

Or with specific focus:
```
/diary focus:decisions
/diary focus:challenges
/diary focus:patterns
/diary focus:assumptions    # Focus on Feynman captures
/diary focus:score-only     # Just run self-evaluation
```

## Automatic Triggers

The diary command can be triggered automatically via hooks:

**PreCompact Hook** (before context compression):
```json
{
  "PreCompact": [{
    "hooks": [{
      "type": "command",
      "command": "claude -p 'Run /diary to capture session learnings'"
    }]
  }]
}
```

**rok-eod Alias** (end of day):
```bash
alias rok-eod='claude -p "/diary" && git add -A && git commit -m "[ROK] Session complete"'
```

## Integration with ROK 3.0

### Learning Loop
```
Session Work → /diary (with Feynman prompts + scoring)
    → Diary Entries
    → /reflect (with anti-pattern detection)
    → CLAUDE.md Updates
    → Better Future Sessions
```

### Expertise Persistence
1. `/diary` captures raw session learnings with Feynman prompts and scores
2. `/reflect` synthesizes across entries, tracking score trends
3. Expertise files (`.md`) store consolidated knowledge
4. Future sessions load expertise automatically
5. Low-scoring patterns become anti-pattern documentation

## Related Commands

| Command | Purpose |
|---------|---------|
| `/search-expertise` | Search ingested expertise files |
| `/reflect` | Synthesize learnings into CLAUDE.md |
| `/1_research` | Research phase (uses expertise search) |

---

**Diary Command v3.1** | ROK 3.6-Feynman Learning Capture + Archon Ingestion
