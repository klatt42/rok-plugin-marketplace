# ROK Plugin Marketplace

## What This Is

Curated collection of 32 Claude Code plugins for domain-specific workflows, multi-agent orchestration, and specialized task automation. Serves as both a public marketplace and a development template for creating new plugins.

## Architecture

Pure markdown + JSON. No build steps, no servers, no database.

```
.claude/marketplace.json          # Master registry (32 plugins)
[plugin-name]/
  .claude-plugin/plugin.json      # Manifest (name, version, description, author)
  commands/*.md                   # Slash commands
  skills/[name]/SKILL.md          # Domain knowledge (YAML frontmatter)
  agents/*.md                     # Subagent definitions (optional)
  scripts/*.py                    # Helper scripts (optional)
  sql/*.sql                       # DB schema (optional)
tests/validate_plugins.py         # Quality validation (Python 3)
PLUGIN_DEV_GUIDE.md               # 7-section dev guide
```

## Plugin Categories

- **Dev workflows**: rok-genesis-core, rok-rpi-workflow, rok-agency-workflows
- **Code quality**: production-code-review, pr-review-toolkit, code-simplifier
- **Business**: deal-management, campaign-management, lead-enrichment
- **Prospecting**: adjuster-prospecting, contractor-prospecting
- **Analysis**: business-idea-analyzer, business-idea-finder, intel-briefing
- **Recommendations**: vehicle-recommender/finder, camper-recommender/finder, medigap-selector
- **Content**: seo-content-optimizer, youtube-intelligence, directory-creator
- **Creative**: banana-squad (image gen), playground
- **Meta**: plugin-idea-generator, claude-code-setup, claude-md-management

## Conventions

- **Plugin names**: kebab-case, must match between directory, plugin.json, and marketplace.json
- **Commands**: kebab-case `.md` files, >100 chars recommended
- **Skills**: YAML frontmatter required (`name`, `description`, `triggers`)
- **Agents**: model specified in YAML (`model: haiku/sonnet/opus`)
- **Versions**: semver in plugin.json
- **Commits**: `[FEATURE] Add plugin-name v1.0.0: description`

## Token Budget (Progressive Disclosure)

- Startup: ~285 tokens (all 32 manifests)
- Skills: ~1757 tokens total (loaded on-demand only)
- Commands: loaded when called

## Validation

```bash
python3 tests/validate_plugins.py    # 6 test suites
claude plugin validate .             # CLI validation
```

Checks: manifest structure, plugin.json quality, command length, skill frontmatter, token budget.

## Installation (Users)

```bash
claude plugin marketplace add https://github.com/klatt42/rok-plugin-marketplace
claude plugin install rok-genesis-core@rok-plugin-marketplace
```

## Creating a New Plugin

1. `mkdir my-plugin && mkdir -p my-plugin/.claude-plugin my-plugin/commands my-plugin/skills`
2. Create `my-plugin/.claude-plugin/plugin.json` with name, version, description, author
3. Add commands as `.md` files in `commands/`
4. Add skills with YAML frontmatter in `skills/[name]/SKILL.md`
5. Register in `.claude/marketplace.json`
6. Run `python3 tests/validate_plugins.py`
7. Commit: `[FEATURE] Add my-plugin v1.0.0`

## Gotchas

- Em dash (--) causes fpdf2 PDF encoding errors; use ASCII hyphen
- YouTube domains need whitelisting in `.claude/settings.local.json`
- Agent model defaults to haiku; specify sonnet/opus when needed
