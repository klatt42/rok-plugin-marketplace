#!/usr/bin/env python3
"""
ROK Plugin Marketplace - Evaluation Tests
==========================================
Validates all plugins in the marketplace meet quality standards.

Run: python3 tests/validate_plugins.py
"""

import json
import os
import sys
import subprocess
from pathlib import Path

MARKETPLACE_ROOT = Path(__file__).parent.parent
PASS = "\033[92m PASS\033[0m"
FAIL = "\033[91m FAIL\033[0m"
WARN = "\033[93m WARN\033[0m"

results = {"pass": 0, "fail": 0, "warn": 0}


def check(name, condition, message=""):
    if condition:
        print(f"  {PASS} {name}")
        results["pass"] += 1
    else:
        print(f"  {FAIL} {name}: {message}")
        results["fail"] += 1


def warn(name, condition, message=""):
    if condition:
        print(f"  {PASS} {name}")
        results["pass"] += 1
    else:
        print(f"  {WARN} {name}: {message}")
        results["warn"] += 1


def test_marketplace_manifest():
    print("\n=== Marketplace Manifest ===")
    manifest_path = MARKETPLACE_ROOT / ".claude-plugin" / "marketplace.json"
    check("marketplace.json exists", manifest_path.exists())

    if not manifest_path.exists():
        return

    data = json.loads(manifest_path.read_text())
    check("has name", "name" in data, "missing 'name' field")
    check("has owner", "owner" in data, "missing 'owner' field")
    check("has plugins list", "plugins" in data and len(data["plugins"]) > 0,
          "missing or empty 'plugins' list")
    warn("has description", "description" in data,
         "add top-level 'description' for discoverability")

    return data.get("plugins", [])


def test_plugin(plugin_entry):
    name = plugin_entry.get("name", "unknown")
    source = plugin_entry.get("source", "")
    plugin_dir = MARKETPLACE_ROOT / source.lstrip("./")

    print(f"\n=== Plugin: {name} ===")

    # Structure
    check("plugin directory exists", plugin_dir.exists(), str(plugin_dir))
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    check("plugin.json exists", manifest.exists())

    if not manifest.exists():
        return

    data = json.loads(manifest.read_text())
    check("has name", "name" in data)
    check("has version", "version" in data)
    check("has description", "description" in data)
    check("has author", "author" in data and "name" in data.get("author", {}))
    check("name matches marketplace entry",
          data.get("name") == name,
          f"manifest says '{data.get('name')}', marketplace says '{name}'")

    desc = data.get("description", "")
    check("description >= 50 chars", len(desc) >= 50,
          f"only {len(desc)} chars — add more detail for discoverability")
    warn("description <= 300 chars", len(desc) <= 300,
         f"{len(desc)} chars — consider trimming for readability")

    # Commands
    cmd_dir = plugin_dir / "commands"
    if cmd_dir.exists():
        cmds = list(cmd_dir.glob("*.md"))
        check(f"has commands ({len(cmds)} found)", len(cmds) > 0)
        for cmd in cmds:
            content = cmd.read_text()
            check(f"  command '{cmd.stem}' not empty", len(content.strip()) > 0)
            warn(f"  command '{cmd.stem}' has instructions (>100 chars)",
                 len(content.strip()) > 100,
                 "command file may be too short to be useful")
    else:
        warn("has commands/ directory", False, "no commands provided")

    # Skills
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        skill_files = list(skills_dir.rglob("SKILL.md"))
        check(f"has skills ({len(skill_files)} found)", len(skill_files) > 0)
        for sf in skill_files:
            content = sf.read_text()
            check(f"  skill '{sf.parent.name}' not empty",
                  len(content.strip()) > 0)

            # Check frontmatter
            has_frontmatter = content.startswith("---")
            check(f"  skill '{sf.parent.name}' has YAML frontmatter",
                  has_frontmatter)

            if has_frontmatter:
                # Extract frontmatter
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    fm = parts[1]
                    check(f"  skill '{sf.parent.name}' frontmatter has 'name'",
                          "name:" in fm)
                    check(f"  skill '{sf.parent.name}' frontmatter has 'description'",
                          "description:" in fm)
                    warn(f"  skill '{sf.parent.name}' frontmatter has 'triggers'",
                         "triggers:" in fm,
                         "add triggers for auto-activation")
    else:
        warn("has skills/ directory", False, "no skills provided")


def test_cli_validation():
    print("\n=== CLI Validation ===")
    try:
        result = subprocess.run(
            ["claude", "plugin", "validate", str(MARKETPLACE_ROOT)],
            capture_output=True, text=True, timeout=15
        )
        passed = "Validation passed" in result.stdout
        check("claude plugin validate passes", passed,
              result.stdout.strip() + result.stderr.strip())
    except FileNotFoundError:
        warn("claude CLI available", False, "claude not in PATH, skipping CLI validation")
    except subprocess.TimeoutExpired:
        warn("claude plugin validate completes", False, "timed out after 15s")


def test_token_budget():
    print("\n=== Token Budget ===")
    total_manifest_chars = 0
    total_skill_chars = 0

    for plugin_dir in MARKETPLACE_ROOT.iterdir():
        if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
            continue
        manifest = plugin_dir / ".claude-plugin" / "plugin.json"
        if manifest.exists():
            total_manifest_chars += manifest.stat().st_size

        for sf in plugin_dir.rglob("SKILL.md"):
            total_skill_chars += sf.stat().st_size

    manifest_tokens = total_manifest_chars // 4
    skill_tokens = total_skill_chars // 4

    check(f"startup cost < 1000 tokens (~{manifest_tokens} tokens)",
          manifest_tokens < 1000,
          f"{manifest_tokens} tokens — reduce manifest descriptions")
    warn(f"total skill content < 50K tokens (~{skill_tokens} tokens)",
         skill_tokens < 50000,
         f"{skill_tokens} tokens — consider splitting large skills")

    print(f"\n  Startup (manifests only): ~{manifest_tokens} tokens")
    print(f"  All skills if triggered:  ~{skill_tokens} tokens")
    print(f"  Progressive disclosure savings: ~{skill_tokens - manifest_tokens} tokens")


def main():
    print("ROK Plugin Marketplace - Evaluation Tests")
    print("=" * 50)

    plugins = test_marketplace_manifest()
    if plugins:
        for p in plugins:
            test_plugin(p)

    test_cli_validation()
    test_token_budget()

    print("\n" + "=" * 50)
    print(f"Results: {results['pass']} passed, {results['fail']} failed, {results['warn']} warnings")

    if results["fail"] > 0:
        print("\nSome tests FAILED. Fix issues above before publishing.")
        sys.exit(1)
    elif results["warn"] > 0:
        print("\nAll tests passed with warnings. Consider addressing them.")
        sys.exit(0)
    else:
        print("\nAll tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
