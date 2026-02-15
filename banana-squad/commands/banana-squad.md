# Banana Squad - Professional Image Generation

Generate professional images using a 4-agent pipeline inspired by PaperBanana research: Research Agent -> Prompt Architect -> Generator Agent -> Critic Agent. Produces 5 image variants with 4-dimension critique scoring.

## Usage

```
/banana-squad:banana-squad Create a professional infographic about global coffee consumption
/banana-squad:banana-squad --refs=/path/to/reference.png Create something in this style about AI investment
/banana-squad:banana-squad A product photo of wireless earbuds --aspect=1:1 --resolution=4K
```

## Arguments

- **description** (optional): What to generate. If omitted, clarifying questions are asked.
- **--refs** (optional): Comma-separated paths to reference images
- **--aspect** (optional): Aspect ratio (default: 16:9). Options: 1:1, 16:9, 9:16, 3:2, 2:3, 4:3, 3:4, 4:5, 5:4, 21:9
- **--resolution** (optional): Resolution (default: 2K). Options: 1K, 2K, 4K (MUST be uppercase)

Initial request: $ARGUMENTS

## Plugin Paths

Set these from the plugin's installation location:

```
PLUGIN_DIR = directory containing this command file, two levels up (the banana-squad plugin root)
SCRIPTS_DIR = PLUGIN_DIR/scripts
AGENTS_DIR = PLUGIN_DIR/agents
REFERENCES_DIR = PLUGIN_DIR/skills/banana-squad/references
```

To find the plugin root, look for the `.claude-plugin/plugin.json` file. The plugin is located at:
`~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad`

## Workflow

### Phase 0: Pre-flight Checks

1. **Check GEMINI_API_KEY**:
   ```bash
   echo $GEMINI_API_KEY | head -c 5
   ```
   If empty, display:
   ```
   GEMINI_API_KEY is not set.

   To set it:
     export GEMINI_API_KEY="your-key-here"

   Or add to a .env file in your working directory:
     GEMINI_API_KEY=your-key-here

   Get a key at: https://aistudio.google.com/apikey
   ```
   **STOP** — do not proceed without the key.

2. **Check Python dependencies**:
   ```bash
   python3 -c "from google import genai; from PIL import Image; print('OK')"
   ```
   If this fails, run the setup script:
   ```bash
   bash ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad/scripts/setup_banana.sh
   ```
   Then re-check. If still failing, display error and **STOP**.

### Phase 1: Requirements Gathering (Lead Role)

Parse `$ARGUMENTS` for any inline flags:
- Extract `--refs=` value (comma-split into list of paths)
- Extract `--aspect=` value (default 16:9)
- Extract `--resolution=` value (default 2K)
- Remaining text is the description

**If description is empty or very brief (< 10 words)**, ask clarifying questions using AskUserQuestion or direct prompting:

1. What should the image depict? (subject, scene, concept)
2. What style? (photorealistic, illustration, icon, sticker, diagram, watercolor, etc.)
3. What mood/tone? (professional, playful, warm, dark, moody, minimalist, vibrant)
4. What aspect ratio? (1:1, 16:9, 9:16, 3:2, 2:3, 4:3, 3:4, 4:5, 5:4, 21:9) — default 16:9
5. What resolution? (1K, 2K, 4K) — default 2K
6. Any text that must appear in the image? Font preference?
7. Any specific reference images to use? (provide exact file path)
8. Where will this be used? (social media, website, print, thumbnail, presentation)
9. Color palette preference? Brand colors?
10. Anything to avoid?

**Wait for user confirmation before proceeding.**

If description is sufficient (>= 10 words with clear intent), confirm with the user:
```
I'll generate images based on:
  Subject: [extracted]
  Style: [inferred or specified]
  Aspect: [value]
  Resolution: [value]
  References: [paths or "none"]

Proceed? (or tell me what to change)
```

### Phase 2: Research Agent (if reference images provided)

**Skip this phase if no reference images were provided.**

Read the Research Agent definition:
```
Read: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad/agents/research-agent.md
```

Launch the Research Agent via Task:

```
Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: """
You are the Research Agent for the Banana Squad image generation pipeline.

[Paste full content of agents/research-agent.md here]

## Your Task

Analyze ONLY these specific reference images:
[list each reference image path]

User requirements:
[paste confirmed requirements]

Output your style brief as JSON.
"""
)
```

Collect result via TaskOutput. This produces the **style brief** JSON.

### Phase 3: Prompt Architect

Read the Prompt Architect definition:
```
Read: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad/agents/prompt-architect.md
```

Read the prompting best practices reference:
```
Read: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad/skills/banana-squad/references/prompting-best-practices.md
```

Launch the Prompt Architect via Task:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
You are the Prompt Architect for the Banana Squad image generation pipeline.

[Paste full content of agents/prompt-architect.md here]

## Prompting Best Practices Reference
[Paste full content of references/prompting-best-practices.md here]

## Your Task

User requirements:
[paste confirmed requirements - subject, style, mood, use case, text requirements, etc.]

Aspect ratio: [value]
Resolution: [value]

Style brief from Research Agent:
[paste style brief JSON from Phase 2, or "No reference images provided — use your best judgment for style"]

Craft 5 distinct narrative image prompts following your instructions. Output as JSON.
"""
)
```

Collect result via TaskOutput. This produces **5 prompts** JSON.

### Phase 4: Generator Agent

Read the Generator Agent definition:
```
Read: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad/agents/generator-agent.md
```

Determine the output directory. Use the user's current working directory + `outputs/` subfolder, or `/tmp/banana-squad-outputs/` if no suitable working directory.

Create a concept slug from the subject (e.g., "coffee-infographic", "earbuds-product").

Launch the Generator Agent via Task:

```
Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: """
You are the Generator Agent for the Banana Squad image generation pipeline.

[Paste full content of agents/generator-agent.md here]

## Your Task

Script path: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad/scripts/generate_image.py

Output directory: [output_dir]
Concept slug: [slug]
Aspect ratio: [value]
Resolution: [value]

Reference image paths: [list of paths, or "none"]

Here are the 5 prompts to generate:

[Paste the full prompts JSON from Phase 3]

Execute each generation, wait 3 seconds between calls, retry on failure. Report results as JSON.
"""
)
```

Collect result via TaskOutput. This produces **generation results** JSON.

### Phase 5: Critic Agent

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
[paste confirmed requirements]

Reference images (if any): [paths or "none"]

Generated images to evaluate:
[For each successful generation, list the output_path]

Read each image file and evaluate on all 4 dimensions. Rank all images and recommend the best one. Output as JSON.
"""
)
```

Collect result via TaskOutput. This produces **critique results** JSON.

### Phase 6: Results Presentation

Parse the critique JSON and present to the user:

```
## Banana Squad Results

### Generated Images

| Rank | Variant | File | Composite | Faith | Read | Concise | Aesthet |
|------|---------|------|-----------|-------|------|---------|---------|
| 1 | v3 Alt Composition | [filename] | 8.35 | 8 | 9 | 8 | 8 |
| 2 | v1 Faithful | [filename] | 7.95 | 8 | 7 | 9 | 8 |
| ...  | ... | ... | ... | ... | ... | ... | ... |

### Top Recommendation: [version] - [label]

[Critic's justification]

### Refinement Suggestions
- [suggestion 1]
- [suggestion 2]
- [suggestion 3]

### Output Location
All images saved to: [output_directory]

---

What would you like to do next?
- Iterate on a specific variant (I'll refine the prompt and regenerate)
- Regenerate all with different parameters
- Accept the results
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Missing GEMINI_API_KEY | Show setup instructions, STOP |
| Missing Python deps | Run setup_banana.sh, retry, STOP if still failing |
| Research Agent fails | Log error, skip to Phase 3 (no style brief) |
| Prompt Architect fails | STOP — cannot continue without prompts |
| Generator: all 5 fail | Report errors clearly, suggest prompt adjustments |
| Generator: some fail | Continue with successful ones, note failures |
| Critic Agent fails | Present images without critique, suggest manual review |

## Rules

- This is the orchestrator — coordinate agents but do NOT generate images yourself
- Always wait for user confirmation before proceeding past Phase 1
- Pipeline is sequential — each phase needs the previous phase's output
- Use `run_in_background: false` for all Task calls (sequential pipeline)
- Present clear, formatted results to the user
- Be transparent about failures — don't hide errors
