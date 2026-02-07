# /yt-brief - Generate Implementation Brief

Transforms a `/yt-analyze` output into a structured implementation brief that feeds directly into `/2_plan` or `/create-prd` workflows. This is the bridge between "I watched a video" and "I'm building something."

## Usage

```
/yt-brief                                    # Use most recent analysis from session
/yt-brief source:thoughts/shared/research/yt-cole-medin-mcp-analysis.md
/yt-brief format:research-input              # Structured for /2_plan
/yt-brief format:prd-input                   # Structured for /create-prd
/yt-brief scope:focused                      # Single-feature brief
```

### Parameters
- **source** - Path to a specific analysis file (default: most recent from session)
- **format** - `brief` (default) | `research-input` (for /2_plan) | `prd-input` (for /create-prd)
- **scope** - `full` (default, all recommendations) | `focused` (user picks one recommendation)

## Execution Steps

### Step 1: Load Analysis

1. If `source:` provided, read the specified file
2. If no source, use the most recent `/yt-analyze` output from the current session
3. If no analysis is available:
   ```
   No analysis found. Run /yt-analyze first, then /yt-brief to generate an implementation brief.
   ```

### Step 2: Select Recommendations

If `scope:focused`:
- List all recommendations from the analysis
- Ask the user to pick which one(s) to build a brief for
- Focus the brief on just the selected items

If `scope:full`:
- Include all recommendations categorized by implementation difficulty

### Step 3: Extract Implementable Items

From the analysis recommendations, identify items that are:
- **Actionable** - Not just informational, has a clear "do this" component
- **Within ROK's technical scope** - Can be implemented with Claude Code plugins, hooks, skills, agents, memory, or existing ROK infrastructure
- **Not contradicting existing ROK decisions** - Cross-reference with memory if available

Filter out:
- Pure informational insights (no action component)
- Items outside ROK's scope (hardware, paid services not already in use, etc.)
- Items already implemented in ROK (check against known capabilities)

### Step 4: Enhancement Research

Use WebSearch to find for each implementable item:
- Official documentation for tools/techniques referenced
- GitHub repos with reference implementations or starter code
- Known issues, limitations, or gotchas not mentioned in the video
- Current version numbers and compatibility notes
- Alternative approaches or complementary techniques

### Step 5: Assess Complexity

For each item, determine the ROK complexity level:
- **SIMPLE** (difficulty 1-2): Single file, < 50 lines, clear pattern to follow
- **MEDIUM** (difficulty 3): Multiple files, some design needed
- **COMPLEX** (difficulty 4-5): Architecture impact, careful planning required

### Step 6: Generate Brief

Generate output in the requested format:

---

#### Format: `brief` (default)

```markdown
# Implementation Brief: [Topic from Video]

**Source:** [Video Title] by [Channel]
**Generated:** [date]
**Overall Confidence:** [HIGH/MEDIUM/LOW]
**Source Analysis:** [path to yt-analyze output]

---

## Problem/Opportunity

[2-3 sentences: What the video revealed that ROK should act on. Why it matters.]

## Proposed Changes

### Change 1: [Name]
- **What:** [Clear description of the change]
- **Where in ROK:** [Specific files, plugins, or systems affected]
- **Complexity:** [SIMPLE/MEDIUM/COMPLEX]
- **Difficulty:** [1-5 scale]
- **Dependencies:** [What must exist or be done first]
- **Estimated effort:** [Brief description]

### Change 2: [Name]
[Same structure]

## Supporting Research
- [URL 1]: [What it confirms or adds beyond the video]
- [URL 2]: [Additional context or reference]

## Implementation Approach Options

### Option A: [Name - Minimal]
[Description, what this covers, what it skips]

### Option B: [Name - Comprehensive]
[Description, what this covers, trade-offs]

## Risks
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|

## Suggested Next Step

[Based on complexity assessment:]
- **If all SIMPLE:** "Ready to implement directly. Start a CC session and reference this brief."
- **If MEDIUM items present:** "Run `/2_plan` with this brief for a detailed implementation plan."
- **If COMPLEX items present:** "Start with `/1_research` to explore codebase implications, then `/2_plan`."

**Command to proceed:**
`/2_plan [path-to-this-brief]`
or
`/create-prd` (then reference this brief in conversation)
```

---

#### Format: `research-input`

Structured to be passed directly to `/2_plan <path>` as the research input document:

```markdown
# Research: [Topic]

**Date:** [date]
**Source:** YouTube Intelligence analysis of "[Video Title]" by [Channel]
**Research Method:** Video transcript analysis + external validation via WebSearch
**Confidence:** [HIGH/MEDIUM/LOW]

## Key Findings

### Finding 1: [Title]
- **Description:** [What was discovered]
- **Evidence:** "[Quote or paraphrase from video]" + [validation source]
- **Confidence:** [HIGH/MEDIUM/LOW]

### Finding 2: [Title]
[Same structure]

## Constraints Identified
- [Technical constraint from video or validation research]
- [ROK architecture constraint]
- [Compatibility or dependency constraint]

## Options Found
- **Option A:** [Approach from video] - [pros/cons]
- **Option B:** [Alternative from validation research] - [pros/cons]
- **Option C:** [Hybrid or ROK-adapted approach] - [pros/cons]

## Open Questions (for /2_plan to address)
- [Question about implementation approach]
- [Question about scope or prioritization]
- [Question about integration with existing ROK systems]

## References
- Video: [URL if available]
- [Supporting URL 1]: [What it provides]
- [Supporting URL 2]: [What it provides]
```

---

#### Format: `prd-input`

Structured to provide the conversation context that `/create-prd` needs to generate a full PRD:

```markdown
# PRD Context: [Feature/Capability Name]

**Origin:** YouTube Intelligence analysis
**Source Video:** "[Title]" by [Channel] ([URL if available])
**Date:** [date]

## Problem Statement
[1-2 paragraphs: What problem does this solve? Derived from video content and validated with research. Written from the perspective of the ROK system user.]

## Target User
- **Who:** [User description - typically ROK system developer/user]
- **Goals:** [What they want to achieve with this capability]
- **Pain Points:** [Current frustrations this addresses]

## Proposed Solution
[2-3 paragraphs: What the video recommends, validated and enhanced with additional research. Adapted for the ROK ecosystem.]

## Requirements

### Must Have (P0)
- [Requirement from video - core functionality]
- [Requirement from video - essential behavior]

### Should Have (P1)
- [Requirement from research - important enhancement]
- [Requirement from research - integration point]

### Nice to Have (P2)
- [Enhancement discovered in research]
- [Future expansion possibility]

## Technical Constraints
- [Existing ROK architecture constraints]
- [Plugin system limitations]
- [Compatibility requirements]
- [Performance considerations]

## Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]

## Prior Art
- [Video source with key takeaway]
- [Related implementations found in research]
- [Existing ROK patterns to build on]

## Open Questions for PRD Author
- [Decision that needs to be made during PRD creation]
```

### Step 7: Save Brief

Save the generated brief to the project's research directory:
- `brief` format: `thoughts/shared/research/yt-brief-[topic-slug]-[date].md`
- `research-input` format: `thoughts/shared/research/yt-research-[topic-slug]-[date].md`
- `prd-input` format: `thoughts/shared/research/yt-prd-context-[topic-slug]-[date].md`

Update the knowledge library entry to set `brief_generated: true`.

### Step 8: Present Next Steps

```
═══════════════════════════════════════════════════════
IMPLEMENTATION BRIEF GENERATED
═══════════════════════════════════════════════════════

Brief saved to: [path]
Format: [brief/research-input/prd-input]

NEXT STEPS:
  /yt-export                      # Export to HTML/PDF/MD for review
  /2_plan [path]                  # Start implementation planning
  /create-prd                     # Generate full PRD (reference the brief)
  /1_research [topic]             # Deeper codebase research first

═══════════════════════════════════════════════════════
```

## Important Rules

- Always trace recommendations back to their video source
- Never generate recommendations that aren't grounded in the analysis
- Enhancement research should ADD to the video's insights, not replace them
- Clearly mark which insights came from the video vs. external research
- Complexity assessments should be conservative (overestimate, not underestimate)
- The brief should be self-contained - a new CC session should be able to act on it without watching the video
