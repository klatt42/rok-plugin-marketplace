# Business Idea Finder

Discover micro-SaaS and AI tool business ideas through pain point mining, gap analysis, and technology arbitrage scanning. Profile-filtered for solopreneur builders. Outputs ranked shortlists that feed into `/business-idea-analyzer:analyze-idea` for deep evaluation.

## Usage

```
/business-idea-finder:find-ideas                                           # Broad scan, all modes, explore depth
/business-idea-finder:find-ideas AI tools for restoration contractors       # Topic-focused, all modes
/business-idea-finder:find-ideas --mode=arbitrage                          # Single mode, broad scan
/business-idea-finder:find-ideas --mode=pain-points --depth=scan           # Quick single-mode scan
/business-idea-finder:find-ideas scheduling tools for home services --depth=deep-scan
```

## Arguments

- **topic** (optional): Seed topic to focus the search. Without a topic, agents scan broadly within profile constraints.
- **--mode** (optional): `pain-points`, `gaps`, `arbitrage`, or `all` (default: `all`). For `--depth=scan`, must specify a single mode.
- **--depth** (optional): `scan` (5-10 min), `explore` (20-40 min, default), `deep-scan` (45-60 min).

Initial request: $ARGUMENTS

## Operator Profile (Hardcoded)

This plugin is hardcoded for this operator. All discoveries are filtered through this profile:

- **Builder type**: Solopreneur using Claude Code, AI-first development
- **Tech stack**: Next.js, Supabase, Chrome extensions, Python, AI APIs
- **Domain expertise**: Home services, restoration, small business operations, insurance
- **Focus**: Micro-SaaS, AI tools, Chrome extensions — "picks and shovels" for business builders
- **Launch timeline**: MVP buildable in <4 weeks, launch-ready Q2 2026
- **Philosophy**: Technology/market arbitrage, 6-12 month opportunity windows
- **EXCLUDED**: E-commerce, dropshipping, real estate, rental properties, investment businesses, consumer apps

## Workflow

### Phase 1: Scope & Discovery Brief

1. **Parse input**: Extract topic (optional), `--mode` flag, `--depth` flag from $ARGUMENTS. Defaults: mode=all, depth=explore.

2. **Validate**: If `--depth=scan` and `--mode=all`, reject with message: "Scan depth requires a single mode. Use `--mode=pain-points`, `--mode=gaps`, or `--mode=arbitrage`."

3. **Discovery search**: Run 2-3 quick WebSearch queries to understand the topic space (if topic provided):
   - `"[topic keywords]" market OR industry OR tools 2026`
   - `"[topic keywords]" small business OR solopreneur OR micro-SaaS`
   Build initial context for the agents.

4. **Build Discovery Brief**:
```
DISCOVERY BRIEF
===============
Topic: [user's topic or "Broad scan — no topic constraint"]
Mode(s): [pain-points, gaps, arbitrage]
Depth: [scan | explore | deep-scan]
Estimated time: [5-10 min | 20-40 min | 45-60 min]
Target shortlist: [5-8 | 10 | 15+ ideas]

Operator Profile:
- Solopreneur, AI-first, micro-SaaS
- Home services / restoration / SMB domain expertise
- Picks-and-shovels philosophy
- <4 week MVP build time
- Excluded: e-commerce, dropshipping, RE, consumer apps

Initial Context:
- [2-3 bullet points from discovery searches, or "Broad scan — agents will explore freely"]
```

5. **Present the Discovery Brief** to the user. Always show this regardless of depth.

6. **APPROVAL GATE** (explore/deep-scan only): Ask the user to confirm or refine scope before proceeding. For `scan` depth, show brief but proceed immediately to Scan Mode.

### Phase 2: Agent Dispatch

#### Scan Mode (depth=scan)
Skip agents entirely. Perform 8-12 WebSearch queries directly using the search patterns from the selected mode's agent definition (read from `agents/[mode-agent].md`). Score results using the shortlist-ranker rubric. Produce 5-8 ideas. Jump to Phase 3.

#### Explore Mode (depth=explore)
Launch 3 research agents simultaneously in a SINGLE message using `Task` with `run_in_background: true`:

| Agent | Subagent Type | Model | Searches | Purpose |
|-------|--------------|-------|----------|---------|
| pain-point-miner | general-purpose | opus | 8-12 | Mine Reddit, forums, reviews for unmet needs |
| gap-analyst | general-purpose | sonnet | 8-12 | Scan Product Hunt, G2, Chrome Store for gaps |
| arbitrage-scanner | general-purpose | opus | 8-12 | Monitor YT creators, HN, AI launches for arbitrage |

If `--mode` is set to a single mode, launch ONLY that mode's agent (still use agents, not direct search).

**For each agent prompt, include**:
1. The agent's full instructions (read from `agents/[agent-name].md` relative to this command)
2. The topic (if provided) or "Broad scan — explore freely within profile constraints"
3. Search count guidance: "Perform 8-12 WebSearch queries."

#### Deep-Scan Mode (depth=deep-scan)
Same as explore but:
- Each agent gets 15-20 searches instead of 8-12
- After the 3 primary agents complete, launch a 4th agent:

| Agent | Subagent Type | Model | Purpose |
|-------|--------------|-------|---------|
| cross-pollinator | general-purpose | opus | Find intersections between the 3 primary agent outputs |

Pass ALL 3 primary agent outputs to the cross-pollinator agent along with its instructions from `agents/cross-pollinator.md`.

### Phase 3: Ranking & Output

1. **Collect results**: Use `TaskOutput` with `block=true` for each agent. Handle failures gracefully — if an agent fails, note it in the final output and proceed with available results.

2. **Launch shortlist-ranker**: Use `Task` (subagent_type: `general-purpose`, model: `sonnet`) with:
   - The ranker's full instructions (read from `agents/shortlist-ranker.md`)
   - All agent outputs concatenated
   - Depth level (determines shortlist size: scan=5-8, explore=10, deep-scan=15)
   - Topic (if any)

3. **Collect ranked shortlist**: The ranker writes to `/tmp/idea_finder_shortlist.json`.

4. **Present shortlist in chat**:

```
## Idea Finder Results: [Topic or "Broad Scan"]

**Date**: [YYYY-MM-DD] | **Depth**: [explore] | **Modes**: [all] | **Ideas found**: [18 raw -> 10 ranked]

### Shortlist

| # | Idea | Tier | Score | Fit | Signal | Type | Window | TAM | Defensibility |
|---|------|------|-------|-----|--------|------|--------|-----|---------------|
| 1 | [Name] | HOT | 85 | 88 | 80 | SaaS | 6-12mo | $30-100M | medium |
| 2 | [Name] | HOT | 82 | 85 | 77 | Extension | 3-6mo | $10-30M | low |
| 3 | [Name] | WARM | 71 | 75 | 65 | SaaS | 12-18mo | $100M+ | high |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Top 3 Detail

**#1: [Idea Name]** (HOT - 85)
> [One-liner pitch]
- Evidence: [Key evidence summary]
- AI advantage: [Why AI matters here]
- Build time: [2-4 weeks]
- Discovered via: [pain-points, arbitrage]
- **Analyze**: `/business-idea-analyzer:analyze-idea [ready-to-paste prompt]`

**#2: [Idea Name]** (HOT - 82)
> [One-liner pitch]
...

**#3: [Idea Name]** (WARM - 71)
> [One-liner pitch]
...

### Profile-Filtered Out (Still Worth Knowing)

Ideas that scored well on opportunity signal but low on profile fit. These may be worth
partnering on, outsourcing, or reconsidering if constraints change.

| Idea | Opportunity Score | Profile Fit | Why Filtered | Worth Revisiting? |
|------|------------------|-------------|--------------|-------------------|
| [Name] | 82 | 35 | Requires mobile-first / network effects | Yes — if partnering |
| ... | ... | ... | ... | ... |

_(If no high-opportunity/low-fit ideas were found, this section is omitted.)_

### Themes
- **Dominant**: [Pattern across top ideas]
- **Emerging niche**: [Specific niche that appeared multiple times]
- **Hottest arbitrage**: [Most time-sensitive opportunity]

### Next Steps
- Pick 1-3 ideas and run `/business-idea-analyzer:analyze-idea [idea]` for deep evaluation
- Run `/business-idea-finder:idea-shortlist` to recall this list later
- Adjust scope and re-run with different `--mode` or `--depth`
```

### Phase 4: Export (optional)

If the user requests export, or for deep-scan depth:
```bash
~/.claude/scripts/.venv/bin/python3 [plugin_scripts_dir]/idea_finder_export.py --input /tmp/idea_finder_shortlist.json
```

Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Idea_Finder/`

## Scan Mode Protocol (depth=scan)

Scan mode skips agents for a fast directional discovery in 5-10 minutes.

**Process**:
1. Require a single `--mode` selection
2. Read that mode's agent definition for its search patterns and source list
3. Run 8-12 WebSearch queries directly following those patterns
4. Score each discovery using the shortlist-ranker rubric (simplified — apply profile fit and opportunity signal inline)
5. Present top 5-8 as a ranked shortlist in chat only — no export, no file generation

**Scan mode does NOT produce**:
- Export files (MD/PDF/HTML)
- Cross-pollination analysis
- Intersection scoring
- Saved shortlist JSON

## Token Budget

| Depth | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Total |
|-------|---------|---------|---------|---------|-------|
| scan | ~2K | ~3K | ~2K | 0 | ~7K |
| explore | ~2K | ~75K | ~8K | ~2K | ~87K |
| deep-scan | ~2K | ~120K | ~15K | ~3K | ~140K |

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate data, statistics, or evidence URLs.
- Present the Discovery Brief and wait for approval (explore/deep-scan) before dispatching agents.
- Handle agent failures gracefully — proceed with available results.
- The `analyze_prompt` in each shortlist entry must be a ready-to-paste command for `/business-idea-analyzer:analyze-idea`.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Idea_Finder/`
- Always filter discoveries through the hardcoded operator profile. Ideas hitting exclusions should rank low, not be silently removed (the user might see value the filter doesn't).
