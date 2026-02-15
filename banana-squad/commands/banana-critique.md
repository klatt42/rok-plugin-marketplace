# Banana Critique - Image Evaluation

Re-critique existing images using the PaperBanana 4-dimension evaluation framework without regenerating. Useful for evaluating images from previous runs or external sources.

## Usage

```
/banana-squad:banana-critique outputs/
/banana-squad:banana-critique /path/to/image.png --requirements="product photo of wireless earbuds"
/banana-squad:banana-critique outputs/ --requirements="infographic about coffee consumption trends"
```

## Arguments

- **image-path-or-folder** (required): Path to a single image or folder of images to critique
- **--requirements** (optional): Original description/requirements to evaluate against. If omitted, the Critic evaluates on general quality.

Initial request: $ARGUMENTS

## Workflow

### Step 1: Parse Arguments

Extract from `$ARGUMENTS`:
- **Image path**: File path or directory path
- **--requirements=**: Original requirements text (if provided)

### Step 2: Discover Images

If path is a directory:
```bash
ls <path>/*.png <path>/*.jpg <path>/*.jpeg <path>/*.webp 2>/dev/null
```

If path is a single file, verify it exists:
```bash
ls -la <path>
```

If no images found, display:
```
No images found at: [path]

Usage: /banana-squad:banana-critique <image-path-or-folder> [--requirements="description"]
```
**STOP.**

### Step 3: Launch Critic Agent

Read the Critic Agent definition:
```
Read: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad/agents/critic-agent.md
```

Launch the Critic Agent via Task:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
You are the Critic Agent for the Banana Squad image generation pipeline.

[Paste full content of agents/critic-agent.md here]

## Your Task

Original user requirements:
[paste requirements, or "No specific requirements provided — evaluate on general image quality"]

Images to evaluate:
[list each image path found in Step 2]

Read each image file and evaluate on all 4 dimensions (Faithfulness, Conciseness, Readability, Aesthetics).

Note: If no specific requirements were provided, score Faithfulness based on internal consistency and clarity of subject matter rather than adherence to a brief.

Rank all images and recommend the best one. Output as JSON.
"""
)
```

Collect result via TaskOutput.

### Step 4: Present Results

```
## Banana Squad Critique

### Image Evaluation

| Rank | Image | Composite | Faith | Read | Concise | Aesthet |
|------|-------|-----------|-------|------|---------|---------|
| 1 | [filename] | 8.35 | 8 | 9 | 8 | 8 |
| 2 | [filename] | 7.95 | 8 | 7 | 9 | 8 |
| ... | ... | ... | ... | ... | ... | ... |

### Top Pick: [filename]

[Critic's justification]

### Per-Image Reviews

**[filename 1]** (Rank #1, Composite: X.XX)
[Review text]

**[filename 2]** (Rank #2, Composite: X.XX)
[Review text]

### Refinement Suggestions
- [suggestion 1]
- [suggestion 2]
- [suggestion 3]

---

To regenerate with improvements, use:
/banana-squad:banana-generate "<refined prompt based on suggestions>"
```

## Plugin Paths

```
Plugin root: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad
Agents: [plugin_root]/agents/critic-agent.md
```

## Rules

- This command ONLY critiques — no generation, no prompt crafting
- Only the Critic Agent is dispatched
- Works with any image format (PNG, JPG, JPEG, WebP)
- If evaluating a single image, still provide full 4-dimension scoring
- `run_in_background: false`
