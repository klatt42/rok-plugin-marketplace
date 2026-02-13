# Plugin Idea Generator

Generate novel Claude Code plugin ideas personalized to your skills, existing plugin portfolio, project history, and current AI trends. Each idea includes a marketization pathway for transitioning from personal tool to sellable product.

## Usage

```
/plugin-idea-generator:generate-ideas                              # Discovery mode, standard depth
/plugin-idea-generator:generate-ideas AI-powered writing tools     # Topic-guided
/plugin-idea-generator:generate-ideas --depth=quick                # Fast brainstorm, no agents
/plugin-idea-generator:generate-ideas --depth=deep                 # Full research + architecture sketches
/plugin-idea-generator:generate-ideas Chrome extensions for devs --depth=standard
```

## Arguments

- **topic** (optional): Focus area for idea generation. Without a topic, agents scan your portfolio gaps + AI trends.
- **--depth** (optional): `quick` (~5 min, no agents), `standard` (~20 min, 3 agents, default), `deep` (~45 min, 3+1 agents + architecture sketches).

Initial request: $ARGUMENTS

## Operator Profile (Hardcoded)

This plugin is hardcoded for this operator. All ideas are filtered through this profile:

- **Builder type**: Solopreneur using Claude Code, AI-first development
- **Tech stack**: Next.js, Supabase, Chrome extensions, Python, Claude API, Stripe
- **Domains**: AI SaaS, marketplace tools, vertical platforms, business intelligence, prospecting, content/SEO
- **Focus**: Picks-and-shovels for builders. Build for yourself first, marketize if valuable.
- **Projects**: 30+ across consumer AI tools, B2B platforms, vertical SaaS, multi-service ecosystems
- **EXCLUDED**: Generic social media apps, gaming, crypto/Web3, dating apps

## Workflow

### Phase 1: Scope & Discovery Brief

1. **Parse input**: Extract topic (optional) and `--depth` flag from $ARGUMENTS. Default: depth=standard.

2. **Live plugin count**: Read the marketplace directory to count current plugins:
   ```
   /home/klatt42/.claude/plugins/marketplaces/rok-plugin-marketplace/*/
   ```

3. **Discovery context**: If topic provided, run 2-3 quick WebSearch queries:
   - `"[topic keywords]" Claude Code plugin OR extension 2026`
   - `"[topic keywords]" AI tool OR agent micro-SaaS 2026`

4. **Build Discovery Brief**:
```
PLUGIN IDEA GENERATOR
=====================
Topic: [user topic or "Open discovery -- scanning portfolio gaps + AI trends"]
Depth: [quick | standard | deep]
Current plugin count: [N] (live scan)
Estimated time: [5 min | 20 min | 45 min]
Target ideas: [5-8 | 12 | 15]

Operator Profile:
- Solopreneur, AI-first, Claude Code + Next.js + Supabase
- 30+ projects, [N] plugins in marketplace
- Picks-and-shovels philosophy
- Excluded: social media apps, gaming, crypto, dating

Initial Context:
- [2-3 bullet points from discovery searches, or "Open discovery -- agents will scan freely"]
```

5. **Present the Discovery Brief** to the user.

6. **APPROVAL GATE** (standard/deep only): Ask the user to confirm or refine scope before proceeding. For `quick` depth, show brief but proceed immediately.

### Phase 2: Agent Dispatch

#### Quick Mode (depth=quick)

Skip agents entirely. Perform research directly:

1. Scan the plugin marketplace directory — read each `plugin.json` to build a quick inventory
2. Run 5-8 WebSearch queries for AI plugin trends:
   - `"Claude Code" plugin idea OR extension 2026`
   - `AI agent tool trending 2026`
   - `VS Code extension AI popular 2026`
   - `"micro-SaaS" AI tool idea 2026`
   - `site:reddit.com r/ClaudeAI plugin wish OR want 2026`
3. Cross-reference: inventory gaps vs. trending patterns
4. Generate 5-8 ideas inline using the scoring rubric from `skills/idea-scoring/SKILL.md`
5. Display in chat only — no export, no JSON file
6. Jump to Phase 5 (Display).

#### Standard Mode (depth=standard)

Launch 2 research agents simultaneously in a SINGLE message using `Task` with `run_in_background: true`:

| Agent | Subagent Type | Model | Purpose |
|-------|--------------|-------|---------|
| portfolio-analyst | general-purpose | sonnet | Scan marketplace, find gaps + extensions |
| trend-scanner | general-purpose | opus | Scan AI news, communities, marketplaces |

**For each agent prompt, include**:
1. The agent's full instructions (read from `agents/[agent-name].md` relative to this command)
2. The topic (if provided) or "Open discovery — scan freely within profile constraints"
3. Search count guidance: "Perform 8-12 WebSearch queries."

**Collect results**: Use `TaskOutput` with `block=true` for each agent. Handle failures gracefully.

**Then launch idea-synthesizer**:

| Agent | Subagent Type | Model | Purpose |
|-------|--------------|-------|---------|
| idea-synthesizer | general-purpose | opus | Combine portfolio + trends into ideas |

Pass both agent outputs + topic to the synthesizer along with its instructions from `agents/idea-synthesizer.md`.

**Collect synthesized ideas**: Use `TaskOutput` with `block=true`.

**Then launch shortlist-ranker**:

| Agent | Subagent Type | Model | Purpose |
|-------|--------------|-------|---------|
| shortlist-ranker | general-purpose | sonnet | Score, rank, tier the ideas |

Pass synthesized ideas + depth level to the ranker along with its instructions from `agents/shortlist-ranker.md`.

#### Deep Mode (depth=deep)

Same as standard but:
- Each research agent gets 15-20 searches instead of 8-12
- The idea-synthesizer generates 18-22 ideas instead of 15-18
- The shortlist-ranker generates architecture sketches for the top 5 ideas
- After ranking, launch idea-synthesizer for a SECOND PASS:
  - Pass the ranked shortlist back to the synthesizer
  - Ask it to find intersection ideas: "Look for ideas that combine 2+ top-ranked concepts"
  - Merge any new intersection ideas into the shortlist and re-rank
- Full export to PDF/HTML/MD after display

### Phase 3: Ranking & Output

1. **Collect ranked shortlist**: The ranker writes to `/tmp/plugin_ideas_shortlist.json`.

2. **Read the shortlist** and prepare display.

### Phase 4: Display

Present results in chat using this template:

```
## Plugin Idea Generator Results

**Date**: [YYYY-MM-DD] | **Depth**: [standard] | **Topic**: [topic or "Open Discovery"]
**Portfolio**: [N plugins scanned] | **Ideas generated**: [20 raw -> 12 ranked]

### Shortlist

| # | Plugin Idea | Tier | Score | Utility | Market | Novelty | Pathway | Extends |
|---|-------------|------|-------|---------|--------|---------|---------|---------|
| 1 | [name]      | BUILD_NOW | 87 | 90 | 85 | 82 | saas_app | -- |
| 2 | [name]      | BUILD_NOW | 83 | 85 | 82 | 78 | chrome_ext | seo-optimizer |
| 3 | [name]      | STRONG | 74 | 78 | 72 | 68 | hybrid | -- |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Top 3 Detail

**#1: [Display Name]** (BUILD_NOW - 87)
> [One-liner description]
- **Why it fits you**: [personal utility rationale]
- **Market signal**: [evidence of demand or 'speculative']
- **AI advantage**: [why AI makes this better]
- **Product pathway**: [pathway] -- [pathway_note with monetization]
- **Proposed structure**: [N] agents, [N] commands, [N] skills
- **Build**: Plugin MVP [1-2 wk] / Product MVP [4-8 wk]
- **Extends**: [existing plugin or "Standalone"]
- **Risk**: [key_risk]
- **Build it**: `/plugin-dev:create-plugin [slug-name]`

**#2: [Display Name]** (BUILD_NOW - 83)
> [One-liner description]
_(same detail format)_

**#3: [Display Name]** (STRONG - 74)
> [One-liner description]
_(same detail format)_

### Portfolio Gap Analysis
- **Covered domains** ([N]): [list]
- **Uncovered domains** ([N]): [list of gaps found]
- **Extension opportunities**: [existing plugins that could spawn companions]

### Themes
- **Dominant**: [Pattern across top ideas]
- **Emerging capability**: [New AI feature driving ideas]
- **Strongest market signal**: [Highest-demand opportunity]

### Next Steps
- Pick an idea and run `/plugin-dev:create-plugin [plugin-name]` to scaffold it
- Run `/plugin-idea-generator:idea-shortlist` to recall this list later
- Re-run with a different topic or depth
```

### Phase 5: Export (deep mode or on request)

```bash
~/.claude/scripts/.venv/bin/python3 [plugin_scripts_dir]/plugin_ideas_export.py --input /tmp/plugin_ideas_shortlist.json
```

Where `[plugin_scripts_dir]` is the `scripts/` directory relative to this plugin.

Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Plugin_Ideas/`

## Token Budget

| Depth | Phase 1 | Phase 2 | Phase 3-4 | Phase 5 | Total |
|-------|---------|---------|-----------|---------|-------|
| quick | ~2K | ~5K | ~2K | 0 | ~9K |
| standard | ~2K | ~80K | ~8K | ~2K | ~92K |
| deep | ~2K | ~130K | ~15K | ~3K | ~150K |

## Rules

- This is a READ-ONLY research tool. Never create plugins, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate data, statistics, or evidence URLs.
- Present the Discovery Brief and wait for approval (standard/deep) before dispatching agents.
- Handle agent failures gracefully — proceed with available results.
- The `create_prompt` in each shortlist entry must be a ready-to-paste `/plugin-dev:create-plugin` command.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Plugin_Ideas/`
- Always filter ideas through the hardcoded operator profile. Ideas hitting exclusions should rank low, not be silently removed.
- Quick mode produces NO files — display in chat only.
