---
name: banana-generate
description: |
  Quick image generation - provide prompt directly, skip clarifying questions.
  Same 4-agent pipeline (Prompt Architect, Generator, Critic) but starts
  immediately from your prompt. Use for fast iteration when you know
  exactly what you want.
triggers:
  - "banana generate"
  - "quick generate"
  - "generate image fast"
  - "quick image"
version: 1.0
author: ROK Agency
---

# Banana Generate

Quick image generation that skips clarifying questions.

## Usage

```
/banana-squad:banana-generate "A photorealistic close-up of fresh strawberries" --aspect=16:9 --resolution=2K
/banana-squad:banana-generate "Minimalist logo in blue and white" --aspect=1:1
```

## When to Use

- When you need to invoke /banana-squad:banana-generate
- When the user's request matches the trigger keywords above
