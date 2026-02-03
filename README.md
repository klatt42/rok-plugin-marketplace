# ROK Plugin Marketplace

Plugins for [Claude Code](https://claude.com/product/claude-code) that add ROK Copilot development workflows, session management, and agency orchestration capabilities.

## Plugins

| Plugin | Description | Commands | Skills |
|--------|-------------|----------|--------|
| **rok-genesis-core** | Session management, learning capture, project initialization with Genesis templates | `session-start`, `session-end`, `diary`, `reflect`, `rok-clean-session`, `project-init` | genesis-core |
| **rok-rpi-workflow** | Research-Plan-Implement methodology with complexity assessment | `1_research`, `2_plan`, `3_implement`, `complexity`, `feynman` | rpi-methodology |
| **rok-agency-workflows** | Multi-agent orchestration, memory system, UI validation | `dispatch`, `spawn-agent`, `memory-query`, `memory-write`, `validate-ui`, `create-prd`, `generate-feature-list` | agency-patterns |

## Installation

```bash
# Add the marketplace
claude plugin marketplace add https://github.com/klatt42/rok-plugin-marketplace

# Install all plugins
claude plugin install rok-genesis-core@rok-plugin-marketplace
claude plugin install rok-rpi-workflow@rok-plugin-marketplace
claude plugin install rok-agency-workflows@rok-plugin-marketplace
```

Once installed, plugins activate automatically in new Claude Code sessions. Skills trigger when relevant, and commands are available via slash prefix (e.g., `/rok-genesis-core:diary`).

## Plugin Structure

Each plugin follows the standard Claude Code plugin format:

```
plugin-name/
├── .claude-plugin/plugin.json   # Manifest (name, version, description)
├── commands/                    # Slash commands (markdown)
└── skills/                      # Domain knowledge (SKILL.md)
```

## Customization

Fork this repo and modify plugins for your team's specific workflows, tools, and conventions. All plugins are file-based (markdown + JSON) with no build steps.

## Requirements

- Claude Code v1.0.33 or later
- Claude Code plugin support enabled

## License

MIT
