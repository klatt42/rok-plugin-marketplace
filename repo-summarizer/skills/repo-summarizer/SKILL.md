---
name: repo-summarizer
description: |
  Trigger skill for the /repo-summarizer:summarize command. Deeply analyzes
  a GitHub or local codebase across 5 dimensions (purpose, features, tech
  stack, gaps, architecture) and produces a scored handoff document for
  another Claude Code session. Supports single repo and multi-repo suite mode.
triggers:
  - "summarize repo"
  - "repo summary"
  - "analyze codebase"
  - "handoff document"
  - "codebase analysis"
  - "repo handoff"
  - "code summary"
version: 1.0
author: ROK Agency
---

# Repo Summarizer Skill

## What It Does

Produces a comprehensive handoff document for a repository that another CC session can consume to quickly understand and work with the codebase.

## When to Use

- Before handing off a repo to a "fix operations" CC session
- When onboarding to a new codebase you haven't seen before
- To audit a repo's maturity level (MATURE/DEVELOPING/EARLY STAGE/PROTOTYPE)
- To analyze a suite of related repos (e.g., FBM apps) for integration planning

## Quick Usage

```
/repo-summarizer:summarize                              # Current directory
/repo-summarizer:summarize ~/projects/my-app            # Local path
/repo-summarizer:summarize https://github.com/user/repo # GitHub URL
/repo-summarizer:summarize user/repo                    # GitHub shorthand
/repo-summarizer:summarize --mode=suite repo1,repo2     # Multi-repo suite
```

## What It Produces

1. **Repo Maturity Score** (0-100) across 5 dimensions:
   - Documentation (15%)
   - Feature Completeness (30%)
   - Infrastructure (20%)
   - Test Presence (15%)
   - Architecture Clarity (20%)

2. **Handoff Brief** -- structured CC-consumable context doc with:
   - Quick navigation table (key files + what they do)
   - Architecture at a glance
   - Known gaps in priority order
   - Key decisions already made
   - What needs attention first

3. **Export Files** (MD + PDF + HTML) to `Desktop/Claude Code Plugin Output/Repo_Summaries/`

## Requirements

- `gh` CLI installed and authenticated (for GitHub repos)
- `~/.claude/scripts/.venv/` with fpdf2 installed (shared venv)

## Analysis Agents

| Agent | Dimension | Model |
|-------|-----------|-------|
| purpose-analyzer | What the repo does | Opus |
| feature-enumerator | Feature inventory + status | Opus |
| stack-analyzer | Tech stack catalog | Sonnet |
| gap-finder | Missing/incomplete functionality | Opus |
| architecture-mapper | Code organization + navigation | Sonnet |
| summary-synthesizer | Merge + score + export | Opus |

## Methodology

For scoring formulas, gap classification taxonomy, and detailed methodology, load the `summarizer-methodology` skill.
