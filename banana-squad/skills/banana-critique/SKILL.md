---
name: banana-critique
description: |
  Re-critique existing images using PaperBanana 4-dimension evaluation
  (Faithfulness, Conciseness, Readability, Aesthetics) without regenerating.
  Point at an image or folder and get scored rankings with refinement
  suggestions.
triggers:
  - "banana critique"
  - "critique image"
  - "evaluate image"
  - "score image"
  - "rate image"
version: 1.0
author: ROK Agency
---

# Banana Critique

Re-critique existing images without regenerating.

## Usage

```
/banana-squad:banana-critique outputs/
/banana-squad:banana-critique /path/to/image.png --requirements="product photo of earbuds"
```

## When to Use

- When you need to invoke /banana-squad:banana-critique
- When the user's request matches the trigger keywords above
