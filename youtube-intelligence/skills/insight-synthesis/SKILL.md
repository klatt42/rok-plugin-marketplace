---
name: insight-synthesis
description: |
  Cross-source insight synthesis, validation, and ROK integration mapping.
  Methodology for combining video insights with external research, cross-
  referencing against ROK memory (decisions, patterns, gotchas), scoring
  implementation difficulty, and generating actionable briefs. Includes
  deduplication, conflict resolution, and learning path construction for
  multi-video analysis. Feeds into /2_plan and /create-prd workflows.
triggers:
  - "synthesize insights"
  - "cross reference"
  - "implementation brief"
  - "learning path"
  - "validate insights"
  - "yt brief"
version: 1.0
author: ROK Agency
---

# Insight Synthesis & ROK Integration

## When to Use This Skill

Use when generating implementation briefs via `/yt-brief`, synthesizing batch results via `/yt-batch`, or cross-referencing video insights with ROK memory.

## Finding Structure

Every synthesized insight should follow this structure:

| Field | Description |
|-------|-------------|
| **Statement** | Core insight in one clear sentence |
| **Source** | Video title, channel, approximate timestamp |
| **Evidence** | Direct quote or paraphrase |
| **Frequency** | How many sources mention this (for batch analysis: 1/N) |
| **Validation** | External confirmation status (confirmed/partial/unconfirmed/contradicted) |
| **Impact** | How much this changes ROK if adopted (high/medium/low) |
| **Confidence** | Combined score from trust + validation + frequency |

## Deduplication Rules (for Batch Analysis)

When multiple videos cover the same insight:
1. **Same insight, same conclusion** - Merge into single entry, increase confidence, cite all sources
2. **Same topic, different perspectives** - Keep both, note the different angles
3. **Contradictory claims** - Flag as conflict, present both sides with evidence, do not pick a winner

**Merge priority**: Use the version with the most evidence and clearest articulation.

## ROK Memory Cross-Reference

For each recommendation from video analysis, check against existing ROK memory:

```
Step 1: Query related decisions
  /memory-query category:"decision" key:"[related-key]" --synthesize

Step 2: Query related patterns
  /memory-query category:"pattern" key:"[related-key]" --synthesize

Step 3: Query related gotchas
  /memory-query category:"gotcha" key:"[related-key]" --synthesize

Step 4: Assess relationship
  - CONFLICT: Recommendation contradicts existing decision → flag for review
  - REINFORCEMENT: Recommendation aligns with existing pattern → increase confidence
  - NEW INSIGHT: No existing memory matches → candidate for memory-write
  - RESOLUTION: Recommendation addresses known gotcha → note as fix
```

If ROK memory (Supabase) is not available, skip this step and note "Memory cross-reference: unavailable".

## Implementation Difficulty Scoring

Score each recommendation on a 1-5 scale:

| Score | Criteria | Example | ROK Workflow |
|-------|----------|---------|--------------|
| **1** | Config change or small addition, single location | Add a new environment variable, update a setting | Implement directly |
| **2** | Single file change, clear existing pattern to follow | New command in existing plugin, new hook script | Implement directly |
| **3** | Multiple files, some design decisions needed | New skill with integration points, new agent | `/2_plan` recommended |
| **4** | Architecture impact, careful planning required | New orchestration pattern, new plugin with agents | `/2_plan` required |
| **5** | System-wide change, high risk, multiple dependencies | Memory system redesign, hook system overhaul | `/1_research` + `/2_plan` required |

## Recommendation Categories

Sort all recommendations into these categories:

### Immediate Actions (difficulty 1-2)
Things that can be done right now in the current CC session. Provide specific instructions.

### Requires Planning (difficulty 3-4)
Things that need a `/2_plan` session. Provide enough context to kickstart the planning.

### Research Further (difficulty 4-5 or low confidence)
Things that need more investigation before acting. Suggest specific research questions.

### Memory Candidates
Insights worth persisting regardless of implementation. Provide ready-to-use `/memory-write` commands:
```
/memory-write category:"pattern" key:"[key]" value:"[insight from video] (source: [channel] [date])"
```

## Brief Generation Formats

### Format: `brief` (default)
General-purpose implementation brief:
```markdown
# Implementation Brief: [Topic]

**Source:** [Video Title] by [Channel]
**Generated:** [date]
**Overall Confidence:** [HIGH/MEDIUM/LOW]

## Problem/Opportunity
[What the video revealed that ROK should act on]

## Proposed Changes
### Change 1: [Name]
- **What:** [description]
- **Where in ROK:** [specific files/systems affected]
- **Complexity:** [SIMPLE/MEDIUM/COMPLEX]
- **Difficulty:** [1-5]
- **Dependencies:** [what must exist first]

## Supporting Research
- [URL 1]: [what it confirms/adds]
- [URL 2]: [what it confirms/adds]

## Risks
| Risk | Impact | Mitigation |
|------|--------|------------|

## Suggested Next Step
[Based on complexity: implement directly / /2_plan / /1_research]
```

### Format: `research-input`
Structured to feed directly into `/2_plan` as the research document input:
```markdown
# Research: [Topic]

**Date:** [date]
**Source:** YouTube Intelligence analysis of [Video Title]
**Research Method:** Video analysis + external validation

## Key Findings
- [Finding 1 with evidence and confidence]
- [Finding 2]

## Constraints Identified
- [Constraint from video or validation research]

## Options Found
- Option A: [approach from video]
- Option B: [alternative from research]
- Option C: [hybrid approach]

## Open Questions
- [Question that /2_plan should address]

## References
- [Video URL]
- [Supporting URLs from validation]
```

### Format: `prd-input`
Structured to provide conversation context for `/create-prd`:
```markdown
# PRD Context: [Feature/Capability]

**Origin:** YouTube Intelligence analysis
**Source Video:** [Title] by [Channel] ([URL])

## Problem Statement
[What problem does this solve, derived from video content]

## Target User
[Who benefits - typically "ROK system user" for methodology improvements]

## Proposed Solution
[What the video recommends, validated and enhanced]

## Requirements
### Must Have
- [P0 requirement from video]

### Should Have
- [P1 requirement from research]

### Nice to Have
- [P2 enhancement discovered in research]

## Technical Constraints
- [Existing ROK architecture constraints]
- [Compatibility requirements]

## Success Criteria
- [Measurable outcome]

## Prior Art
- [Video source]
- [Related implementations found in research]
```

## Learning Path Construction (Batch)

When `/yt-batch` produces multiple analyzed videos, construct a suggested watch/study order:

1. **Identify prerequisite knowledge** for each video
2. **Order from foundational to advanced** based on concept dependencies
3. **Insert non-video resources** between videos where helpful (official docs, repos, tutorials)
4. **Note what each video builds upon** from earlier entries

```markdown
### Suggested Learning Path: [Topic]

1. **[Video A Title]** by [Channel] - Foundational concepts
   - Covers: [key topics]
   - Prerequisites: None

2. **[Official Docs Link]** - Reference reading
   - Read before next video for context

3. **[Video B Title]** by [Channel] - Builds on #1
   - Covers: [key topics]
   - Prerequisites: Concepts from Video A

4. **[Video C Title]** by [Channel] - Advanced application
   - Covers: [key topics]
   - Prerequisites: Videos A + B
```

## Knowledge Library Indexing

After every analysis, append to `~/.claude/youtube-intelligence/library.json`:

```json
{
  "video_id": "[YouTube video ID or slug]",
  "title": "[Video title]",
  "channel": "[Channel name]",
  "url": "[YouTube URL if available]",
  "analyzed": "[ISO date]",
  "type": "[content classification]",
  "topics": ["topic1", "topic2"],
  "trust_weight": "HIGH|MEDIUM|STANDARD",
  "key_points_count": 7,
  "claims_count": 3,
  "recommendations_count": 4,
  "analysis_path": "[path to saved analysis file]",
  "brief_generated": false
}
```

If library.json does not exist, create it with `{"videos": []}` structure first.
