# Plugin Inventory

Display current plugin portfolio with domain categorization, gap analysis, and extension opportunities.

## Usage

```
/plugin-idea-generator:plugin-inventory                  # Full inventory + gap analysis
```

## Arguments

None required.

Initial request: $ARGUMENTS

## Workflow

1. **Scan marketplace**: Read every `plugin.json` in:
   ```
   /home/klatt42/.claude/plugins/marketplaces/rok-plugin-marketplace/*/.claude-plugin/plugin.json
   ```

2. **For each plugin**, extract:
   - Name, version, description
   - Count of files in `agents/` directory
   - Count of files in `commands/` directory
   - List of subdirectories in `skills/`
   - Whether `scripts/` exists

3. **Categorize** each plugin by domain:
   - `business-dev` — Business ideas, market analysis, deal management
   - `research` — Intelligence, YouTube analysis, content research
   - `prospecting` — Lead gen, campaigns, outreach
   - `recommendations` — Vehicle/camper recommender-finder pairs
   - `code-quality` — Code review, production review
   - `content` — SEO, content optimization
   - `core-infra` — Plugin development, hooks, system tools
   - `legal` — Legal case building
   - `data-analysis` — Data exploration, visualization
   - `personal-productivity` — Task management, workflows
   - `finance` — Financial analysis
   - `social-media` — Social media management
   - `project-management` — Project tracking
   - `client-delivery` — Client portals, reporting

4. **Display**:

```
## Plugin Portfolio Inventory

**Scan date**: [YYYY-MM-DD] | **Plugins found**: [N] | **Total agents**: [N]

### By Domain

| Domain | Plugins | Names |
|--------|---------|-------|
| business-dev | 3 | business-idea-finder, business-idea-analyzer, deal-management |
| research | 2 | intel-briefing, youtube-intelligence |
| recommendations | 4 | vehicle-recommender, vehicle-finder, camper-recommender, camper-finder |
| ... | ... | ... |

### Coverage Map

| Covered ([N]) | Uncovered ([N]) |
|---------------|-----------------|
| business-dev, research, ... | personal-productivity, finance, ... |

### Plugin Details

| Plugin | Version | Agents | Commands | Skills | Export |
|--------|---------|--------|----------|--------|--------|
| business-idea-finder | 1.2.0 | 5 | 2 | 2 | Yes |
| ... | ... | ... | ... | ... | ... |

### Extension Opportunities

Patterns from the portfolio that could spawn companion plugins:

- **[existing]** -> [companion idea] ([pattern type])
- ...

### Upgrade Candidates

Plugins that could benefit from expansion:

| Plugin | Version | Agents | Reason |
|--------|---------|--------|--------|
| ... | 1.0.0 | 1 | Single agent, no skills, no export |

### Portfolio Stats

- Average agents per plugin: [N]
- Most complex plugin: [name] ([N] agents)
- Most recent version: [name] v[N]
- Plugins with export: [N] of [M]
- Plugins with skills: [N] of [M]

### Next Steps
- Run `/plugin-idea-generator:generate-ideas` to discover new plugin ideas based on this inventory
- Run `/plugin-idea-generator:generate-ideas [topic]` to focus idea generation on a specific domain
```

## Rules
- This is a READ-ONLY scan. Never modify any files.
- Report actual counts — don't estimate.
- If a plugin directory lacks a valid plugin.json, skip it and note it.
- A plugin can belong to multiple domains.
- Include the extension opportunities section — this is the most actionable part.
