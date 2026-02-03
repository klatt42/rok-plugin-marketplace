# /reflect Command

Synthesize learnings across multiple diary entries to identify patterns, update expertise files, and recommend CLAUDE.md enhancements.

**Version**: 3.0 (ROK 3.6-Feynman - Enhanced with Anti-Pattern Detection & Score Aggregation)

## Execution Steps

### 1. Gather Diary Entries
```bash
# Find all diary entries since last reflection
ls -la ~/.claude/expertise/*-diary-*.md

# Check last reflection timestamp
cat ~/.claude/expertise/.last-reflect
```

Read all entries created since last /reflect (check for `reflection-*.md` timestamps).

### 2. Aggregate Assumption-Corrections

Scan all diary entries for "Assumption Corrections" sections.

Group by theme:
- Codebase assumptions (how this project works)
- Technology assumptions (how tools/libraries behave)
- Process assumptions (how workflows should proceed)
- User assumptions (what the user actually needs)

Identify recurring corrections:
- Same assumption corrected multiple times = needs explicit documentation
- Related corrections = underlying mental model needs update

### 3. Detect Anti-Patterns

Scan diary entries for signs of cognitive anti-patterns (from `~/.claude/expertise/anti-patterns.md`):

| Anti-Pattern | Detection Signal |
|--------------|-----------------|
| Pattern Matching | "I assumed it was like X but..." |
| Assumption Skipping | Multiple corrections about same system |
| Premature Commitment | "Should have considered..." entries |
| Jargon Masking | Corrections about misunderstood terms |
| Success Theater | "Worked but I didn't understand why" |
| Russian Roulette | "We've always done it this way" failures |

For each detected anti-pattern:
1. Document the instance
2. Identify the trigger condition
3. Propose a correction rule
4. Update personal high-frequency tracking

### 4. Aggregate Scores

Collect all self-assessment scores from diary entries:

```markdown
## Score Trends (Last Period)

| Date | Project | Completion | Quality | Efficiency | Learning | Communication | Avg |
|------|---------|------------|---------|------------|----------|---------------|-----|
| [date] | [project] | X | X | X | X | X | X.X |

**Period Average**: X.X/10
**Sessions Below Bar (< 7)**: N/N (X%)
**Trend**: Improving/Stable/Declining

### Low-Score Analysis
- [Criterion] scored low in [N] sessions because [pattern]

### High-Score Patterns
- [Criterion] consistently high when [condition]
```

### 5. Extract Proven Strategies

From "Pattern Discoveries" and successful "Problems & Solutions":
- Identify approaches that worked consistently
- Note conditions where they succeeded
- Note any failures of the same approach (edge cases)

### 6. Generate Expertise File Updates

For each project with diary entries:

```markdown
# Proposed Updates to: ~/.claude/expertise/[project].md

## New Proven Patterns
[patterns extracted from diaries]

## New Disproven Assumptions
[assumption-corrections consolidated]

## Updated Mental Models
[refined understanding from multiple entries]

## New Decision Rationale
[decisions worth preserving for future reference]
```

### 7. Generate CLAUDE.md Recommendations

Based on cross-cutting patterns:

```markdown
# Proposed CLAUDE.md Updates

## New Anti-Pattern Rules
[if recurring anti-patterns detected]

## New Complexity Signals
[if certain task types consistently needed full protocol]

## Process Refinements
[if workflow improvements discovered]
```

### 8. Apply Updates (With Approval)

Present proposed changes to user:
1. Show diff for each expertise file
2. Show diff for CLAUDE.md
3. Request approval before applying
4. Create backup before modifying

### 9. Record Reflection

Create reflection log:
`~/.claude/expertise/reflection-[YYYY-MM-DD].md`

Contents:
- Entries processed
- Updates applied
- Patterns identified
- Score trends
- Next reflection recommended date

## Output Format

```markdown
# Reflection Summary: [YYYY-MM-DD]

## Entries Processed
- [list of diary files analyzed]

## Score Summary

### Period Scores
| Date | Project | Avg Score | Quality Bar |
|------|---------|-----------|-------------|
| [date] | [project] | X.X | Met/NOT MET |

**Period Average**: X.X/10
**Sessions Below Bar**: N/N (X%)
**Trend**: [direction]

### Score Patterns
- Highest: [criterion] - [why it's strong]
- Lowest: [criterion] - [action to improve]

## Key Findings

### Recurring Assumption-Corrections
| Theme | Correction | Frequency | Action Taken |
|-------|------------|-----------|--------------|
| [theme] | [what was wrong] | [count] | [expertise update] |

### Anti-Patterns Detected
| Pattern | Instances | Trigger | Mitigation Added |
|---------|-----------|---------|------------------|
| [name] | [count] | [cause] | [rule added] |

### Proven Strategies Extracted
| Strategy | Success Context | Added To |
|----------|-----------------|----------|
| [name] | [when it works] | [file] |

## Updates Applied
- [file]: [change summary]

## Recommendations for Next Period
- [suggested focus areas]

---
*Reflection performed by /reflect command v3.0*
```

## Usage

```
/reflect
```

Or with options:
```
/reflect since:2025-01-01     # Specific date range
/reflect project:rok-copilot  # Single project
/reflect dry-run              # Show without applying
/reflect scores-only          # Just score aggregation
```

## Recommended Cadence

- **Weekly**: Full reflection with all diary entries
- **Monthly**: Deep reflection including CLAUDE.md updates
- **After low-score session**: Immediate mini-reflection

## Integration Points

### With /diary
- /diary creates entries with Feynman prompts and scores
- /reflect consumes and synthesizes entries
- Creates virtuous learning loop

### With anti-patterns.md
- /reflect checks diary entries against known anti-patterns
- Updates anti-patterns.md with new patterns discovered
- Tracks personal high-frequency anti-patterns

### With Expertise Files
- Proposes updates based on consolidated learnings
- Maintains structured format from TEMPLATE.md
- Archives decision rationale

### With CLAUDE.md
- Recommends cross-cutting updates
- New complexity signals
- Process refinements

## Score History File Format

Store historical data in `~/.claude/expertise/.score-history`:

```csv
date,project,completion,quality,efficiency,learning,communication,average,bar_met
2025-12-23,rok-system,9,9,8,9,9,8.8,true
2025-12-22,bizcopilot,9,8,7,8,9,8.2,true
```

This enables long-term trend analysis across weeks/months.

---

**Reflect Command v3.0** | ROK 3.6-Feynman Synthesis with Anti-Pattern Detection
