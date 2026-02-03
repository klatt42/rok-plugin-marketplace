# Plugin Development Guide

How to create, test, and publish plugins for this marketplace.

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: manifest
├── commands/                 # Optional: slash commands
│   ├── my-command.md
│   └── another-command.md
└── skills/                   # Optional: domain knowledge
    └── my-skill/
        └── SKILL.md
```

## 1. Create plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "50-300 chars. Include trigger keywords for discoverability.",
  "author": {
    "name": "Your Name"
  }
}
```

**Rules:**
- `name` must match the directory name and marketplace entry
- `description` must be 50-300 characters
- Include keywords that help Claude match the plugin to user requests

## 2. Add Commands

Commands are markdown files in `commands/`. Each file becomes a slash command (e.g., `commands/deploy.md` -> `/my-plugin:deploy`).

```markdown
# Deploy Command

You are executing a deployment workflow.

## Steps
1. Run the build
2. Verify tests pass
3. Deploy to production

## Rules
- Always run tests before deploying
- Never deploy on Friday after 3pm
```

**Rules:**
- File must be >100 characters to be useful
- Name the file after the command (no spaces, use hyphens)
- Write instructions as if talking to Claude

## 3. Add Skills

Skills are `SKILL.md` files with YAML frontmatter. They provide domain knowledge that loads when triggered.

```markdown
---
name: my-skill
description: |
  50-100 words describing what this skill covers.
  Include trigger keywords for auto-activation.
triggers:
  - "keyword phrase"
  - "another trigger"
version: 1.0
author: Your Name
---

# Skill Title

## Section 1
Content that helps Claude understand the domain...

## Section 2
More structured knowledge...
```

**Rules:**
- Frontmatter must include `name`, `description`
- `triggers` are recommended for auto-activation
- Skills load on-demand (not at startup), so they can be detailed

## 4. Add to Marketplace

Edit `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./my-plugin",
      "description": "Brief description for marketplace listing."
    }
  ]
}
```

The `name` must match `plugin.json` name exactly.

## 5. Validate

```bash
# Run evaluation tests
python3 tests/validate_plugins.py

# Run CLI validation
claude plugin validate .
```

**Quality checklist:**
- [ ] plugin.json has name, version, description, author
- [ ] Description is 50-300 characters
- [ ] All commands are >100 characters
- [ ] Skills have YAML frontmatter with name + description
- [ ] Name matches between plugin.json and marketplace.json
- [ ] `claude plugin validate` passes

## 6. Token Budget

Manifests load at startup. Skills load on trigger. Keep manifests lean.

| Component | Budget | When Loaded |
|-----------|--------|-------------|
| plugin.json | <250 tokens each | Session start |
| Commands | Varies | On slash command |
| Skills | <5K tokens each | On trigger match |

Current marketplace: ~285 tokens startup, ~1757 tokens all skills.

## 7. Publish

```bash
git add .
git commit -m "[FEATURE] Add my-plugin"
git push
```

Users install with:
```bash
claude plugin marketplace add https://github.com/klatt42/rok-plugin-marketplace
claude plugin install my-plugin@rok-plugin-marketplace
```
