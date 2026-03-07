# Banana Generate - Quick Image Generation

Quick image generation that skips clarifying questions. Provide your prompt directly and get 5 variants with critique scoring. Same pipeline as `/banana-squad:banana-squad` but starts at Phase 2/3.

## Usage

```
/banana-squad:banana-generate "A photorealistic close-up of fresh strawberries on a rustic wooden table, morning golden hour light" --aspect=16:9 --resolution=2K
/banana-squad:banana-generate "Minimalist tech startup logo with geometric shapes in blue and white" --aspect=1:1 --variants=3
/banana-squad:banana-generate "Dark moody product photo of a luxury watch" --refs=/path/to/ref.png --aspect=4:5 --resolution=4K
```

## Arguments

- **prompt** (required): Full descriptive prompt text (in quotes)
- **--refs** (optional): Comma-separated paths to reference images
- **--aspect** (optional): Aspect ratio (default: 16:9)
- **--resolution** (optional): Resolution (default: 2K)
- **--variants** (optional): Number of variants (1-5, default: 5). Fewer = faster + cheaper.

Initial request: $ARGUMENTS

## Workflow

### Phase 0: Pre-flight Checks

Same as `/banana-squad:banana-squad`:
1. Check `GEMINI_API_KEY` exists
2. Check Python dependencies installed

If either fails, show setup instructions and STOP.

### Phase 1: Parse Arguments

Extract from `$ARGUMENTS`:
- **Prompt text**: Everything in quotes, or all text not matching flags
- **--refs=**: Comma-split into reference image paths
- **--aspect=**: Aspect ratio (default 16:9)
- **--resolution=**: Resolution (default 2K)
- **--variants=**: Number of variants (default 5, must be 1-5)

If no prompt text is found, display:
```
Usage: /banana-squad:banana-generate "<your prompt>" [--aspect=16:9] [--resolution=2K] [--refs=path1,path2]

The prompt should be a descriptive paragraph. For guided generation with questions, use:
/banana-squad:banana-squad
```
**STOP.**

Confirm to user:
```
Quick generating with:
  Prompt: [first 100 chars]...
  Aspect: [value]
  Resolution: [value]
  References: [count or "none"]
```

### Phase 2: Research Agent (if references provided)

**Skip if no reference images.**

Same as `/banana-squad:banana-squad` Phase 2:
- Read `agents/research-agent.md`
- Launch Research Agent via Task with reference paths
- Collect style brief JSON

### Phase 3: Prompt Architect

Same as `/banana-squad:banana-squad` Phase 3:
- Read `agents/prompt-architect.md` and `references/prompting-best-practices.md`
- Launch Prompt Architect with user's prompt as the primary input
- Pass `--variants` count (the user's prompt becomes the basis for v1 Faithful, with v2-vN as creative variations)
- Collect prompts JSON (1-5 prompts based on variants setting)

### Phase 4: Generator Agent

Same as `/banana-squad:banana-squad` Phase 4:
- Read `agents/generator-agent.md`
- Launch Generator Agent with prompts, **both script paths** (generate_image.py + generate_batch.py), output directory
- Uses parallel generation via `generate_batch.py` (default 3 concurrent workers)
- Collect generation results JSON

### Phase 5: Critic Agent

Same as `/banana-squad:banana-squad` Phase 5:
- Read `agents/critic-agent.md`
- Launch Critic Agent with generated image paths and original prompt
- Collect critique results JSON

### Phase 6: Save Session & Generate Gallery

Same as `/banana-squad:banana-squad` Phase 6:
- Save `session.json` to output directory (prompts, scores, rankings)
- Run `generate_gallery.py --dir [output_dir]` to create `index.html`
- Open gallery in browser

### Phase 7: Results Presentation

Same format as `/banana-squad:banana-squad` Phase 7.

## Plugin Paths

```
Plugin root: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad
Scripts: [plugin_root]/scripts/generate_image.py
Agents: [plugin_root]/agents/
References: [plugin_root]/skills/banana-squad/references/
```

## Plugin Paths (Updated)

```
Plugin root: ~/.claude/plugins/marketplaces/rok-plugin-marketplace/banana-squad
Scripts:
  - generate_image.py  (single image generation)
  - generate_batch.py  (parallel batch generation)
  - generate_gallery.py (gallery HTML generator)
Agents: [plugin_root]/agents/
References: [plugin_root]/skills/banana-squad/references/
```

## Rules

- Do NOT ask clarifying questions — the user provided everything
- If the prompt is too vague, still proceed (Prompt Architect will handle variation)
- Same error handling as `/banana-squad:banana-squad`
- Pipeline is sequential between phases, but image generation within Phase 4 is parallel
- Use `run_in_background: false` for Task calls (phases are sequential)
- Always save session.json and generate gallery after critique
