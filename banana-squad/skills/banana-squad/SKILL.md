---
name: banana-squad
description: |
  Multi-agent professional image generation using Gemini 3 Pro Image API.
  Implements PaperBanana research pipeline with 4 specialized agents:
  Research Agent (style analysis), Prompt Architect (5-variant prompts),
  Generator Agent (Gemini API calls), Critic Agent (4-dimension scoring).
  Use for professional images, infographics, product photos, diagrams,
  thumbnails, marketing visuals, or any styled image generation task.
triggers:
  - "banana squad"
  - "banana-squad"
  - "generate images"
  - "image generation"
  - "paperbanana"
  - "nano banana"
version: 1.0
author: ROK Agency
---

# Banana Squad

Multi-agent image generation pipeline inspired by PaperBanana research.

## Commands

| Command | Purpose |
|---------|---------|
| `/banana-squad:banana-squad` | Full pipeline with clarifying questions |
| `/banana-squad:banana-generate` | Quick generate - provide prompt directly |
| `/banana-squad:banana-critique` | Re-critique existing images |

## Pipeline

1. **Research Agent** - Analyzes reference images, extracts style brief
2. **Prompt Architect** - Crafts 5 narrative prompt variants
3. **Generator Agent** - Calls Gemini API, saves 5 PNGs
4. **Critic Agent** - Scores on Faithfulness, Conciseness, Readability, Aesthetics

## Reference Docs (load on demand)

- `references/gemini-api-guide.md` - Full Gemini 3 Pro Image API reference
- `references/paperbanana-summary.md` - PaperBanana research insights
- `references/prompting-best-practices.md` - Image prompt crafting guide

## When to Use

- When a user asks to generate images or visual content
- When a user mentions PaperBanana, Banana Squad, or Nano Banana
- When professional image generation with critique is needed
