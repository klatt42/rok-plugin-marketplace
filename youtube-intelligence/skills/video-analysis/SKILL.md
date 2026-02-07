---
name: video-analysis
description: |
  YouTube video content extraction, transcript processing, and structured
  summarization methodology. Includes content type classification (tutorial,
  thought-leadership, news, demo-walkthrough, discussion, case-study), key
  point extraction patterns, technical detail capture for code-heavy videos,
  and claim identification for validation. Handles auto-generated and manual
  transcripts with noise filtering.
triggers:
  - "youtube video"
  - "video analysis"
  - "transcript analysis"
  - "video summary"
  - "youtube transcript"
  - "analyze video"
version: 1.0
author: ROK Agency
---

# Video Analysis Methodology

## When to Use This Skill

Use when processing YouTube video content for analysis via `/yt-analyze` or `/yt-batch`. This skill provides the classification, extraction, and structuring methodology.

## Content Type Classification

Classify each video into exactly one type based on transcript content, title, and description:

| Type | Signal Patterns | Analysis Focus |
|------|----------------|----------------|
| `tutorial` | "step by step", "how to", "let me show you", numbered instructions, "follow along" | Extract steps, tools, code, dependencies, prerequisites |
| `thought-leadership` | "I believe", "the future of", "my take", "here's why", opinion markers, predictions | Extract thesis, arguments, predictions, strategic implications |
| `news` | "just announced", "breaking", dates, version numbers, "released today", "update" | Extract facts, timelines, implications, what changed |
| `demo-walkthrough` | "let me demo", "as you can see", UI descriptions, "click here", screen references | Extract tool names, features, workflows, configuration |
| `discussion` | Multiple speakers, "what do you think", Q&A format, interview structure | Extract each speaker's position, consensus points, disagreements |
| `case-study` | "we built", "our experience", metrics, results, "lessons learned", retrospective | Extract approach, metrics, lessons learned, what they'd do differently |

When ambiguous, prefer the type that best serves extraction. A tutorial that includes opinions is still a `tutorial`.

## Transcript Processing

### Input Methods (cascade priority)
1. **User pasted transcript** - Use directly, highest quality since user curated it
2. **File path provided** - Read with Read tool
3. **URL with yt-dlp available** - Run: `yt-dlp --write-auto-sub --sub-lang en --skip-download -o "%(title)s" <url>` then read the .vtt/.srt file
4. **URL with WebFetch** - Fetch YouTube page, extract available metadata + description
5. **No transcript obtained** - Ask user to paste transcript or provide file

### Auto-Generated Transcript Cleanup
- Filter filler words only when they obscure meaning ("um", "uh", "you know", "like" as filler)
- Fix common speech-to-text errors for technical terms (e.g., "cloud code" -> "Claude Code", "MPC" -> "MCP")
- Preserve technical terms exactly: model names, library names, CLI commands, URLs
- Identify speaker changes when multiple voices are present
- Note transcript quality: HIGH (manual captions), MEDIUM (auto-generated, clear), LOW (auto-generated, noisy)

## Key Point Extraction Framework

Extract up to 10 key points. Each key point must have:

| Field | Description | Example |
|-------|-------------|---------|
| **Statement** | Core insight in one clear sentence | "MCP servers can cache tool results for 15 minutes to reduce API calls" |
| **Evidence** | Direct quote or paraphrase from video | "As Cole says at ~12:00, 'adding a simple cache layer cut our API calls by 80%'" |
| **Confidence** | How clearly stated (explicit/implied/speculative) | `explicit` - directly stated as recommendation |
| **Actionability** | Can this be acted on? (high/medium/low/informational) | `high` - specific technique that can be implemented |

### Prioritization Rules
1. Actionable insights over informational ones
2. Novel insights over commonly known ones
3. Specific techniques over general philosophy
4. Quantified claims over qualitative ones

## Technical Detail Extraction

For tutorial, demo-walkthrough, and case-study videos, also extract:

### Tools & Technologies
```
| Tool/Library | Version (if mentioned) | Context | URL/Repo |
|-------------|----------------------|---------|----------|
| Claude Code | latest | Primary development tool | - |
| yt-dlp | 2024.x | Transcript extraction | github.com/yt-dlp/yt-dlp |
```

### Code Patterns
- Extract any code snippets described (even verbally)
- Note configuration values or settings mentioned
- Capture architecture patterns described
- Record CLI commands or terminal operations shown

### Dependencies & Prerequisites
- What must be installed first
- Required accounts or API keys
- Version compatibility notes

## Claim Identification

A "claim" is any factual assertion that can be independently verified via web search. Tag each claim with a type:

| Claim Type | Example | Verification Approach |
|-----------|---------|----------------------|
| `performance` | "X is 3x faster than Y" | Search for benchmarks, comparisons |
| `capability` | "Claude can now process images in real-time" | Search for official docs, release notes |
| `best-practice` | "You should always use environment variables for API keys" | Search for security guidelines, docs |
| `comparison` | "MCP is better than function calling because..." | Search for comparisons, alternative viewpoints |

### What Is NOT a Claim
- Opinions clearly stated as opinions ("I prefer X")
- Future predictions ("I think X will happen")
- Personal experiences ("In my project, X worked well")

## Output Structure

```markdown
## Video Analysis: [Title]

**Channel:** [name] [TRUSTED CREATOR badge if applicable]
**Published:** [date] | **Duration:** [length] | **Type:** [classification]
**Transcript Quality:** [HIGH/MEDIUM/LOW]
**Trust Weight:** [HIGH/STANDARD] - [reason]

### Key Points
1. **[Statement]** (actionability: high)
   - Evidence: "[quote or paraphrase]"

2. **[Statement]** (actionability: medium)
   - Evidence: "[quote or paraphrase]"

[up to 10 key points]

### Technical Details
| Tool | Version | Context |
|------|---------|---------|
[if applicable]

### Code Patterns & Commands
[if applicable]

### Quotable Statements
- "[Direct quote]" - [context for when to reference]

### Claims to Validate
- [ ] [Claim 1] (type: performance) - [search suggestion]
- [ ] [Claim 2] (type: capability) - [search suggestion]
```
