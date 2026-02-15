# PaperBanana Research Summary

> Condensed from: Zhu et al. (2026). "PaperBanana: Automating Academic Illustration for AI Scientists." Peking University & Google Cloud AI Research. arXiv:2601.23265v1

## Core Concept

PaperBanana is an agentic framework for automated generation of publication-ready academic illustrations. It orchestrates 5 specialized agents powered by VLMs and Gemini 3 Pro Image API (Nano Banana Pro) to transform scientific content into professional diagrams and plots.

## 5-Agent Architecture

| Agent | Role | Our Equivalent |
|-------|------|----------------|
| **Retriever** | Finds relevant reference examples by matching research domain and diagram type. Visual structure prioritized over topic similarity. | Research Agent |
| **Planner** | Cognitive core. Translates unstructured data into comprehensive textual descriptions using in-context learning from retrieved examples. | Prompt Architect |
| **Stylist** | Design consultant. Synthesizes aesthetic guidelines (color palette, shapes, lines, layout, typography) from reference collection. Refines descriptions for visual polish. | Prompt Architect |
| **Visualizer** | Renders images from optimized descriptions using image generation model. Iterates with Critic for T=3 rounds. | Generator Agent |
| **Critic** | Examines generated images against source context. Identifies misalignments, provides targeted feedback, produces refined descriptions. | Critic Agent |

## Pipeline Flow

```
Input (description + caption)
  -> Retriever (find N reference examples)
  -> Planner (create detailed textual description P)
  -> Stylist (refine P -> P* with aesthetic guidelines)
  -> Visualizer + Critic loop (3 iterations)
  -> Final image
```

## 4 Evaluation Dimensions

Inspired by Quispel et al. (2018) information visualization research:

### Primary Dimensions (take precedence in scoring)

| Dimension | Definition | What to Check |
|-----------|-----------|---------------|
| **Faithfulness** | Alignment with source context and communicative intent | Correct elements, accurate data, correct relationships, no hallucinated content |
| **Readability** | Layout clarity, text legibility, composition cleanliness | Intelligible layouts, legible text, clear hierarchy, no excessive crossing lines, intuitive flow |

### Secondary Dimensions

| Dimension | Definition | What to Check |
|-----------|-----------|---------------|
| **Conciseness** | Focus on core information without visual clutter | Core message focus, intentional white space, no unnecessary elements |
| **Aesthetics** | Adherence to professional stylistic norms | Cohesive palette, consistent typography, proper alignment, visual balance |

### Hierarchical Scoring

The evaluation hierarchy is: **Faithfulness > Readability > Conciseness > Aesthetics**.

If primary dimensions (Faithfulness, Readability) yield a decisive winner, that determines the overall result. Secondary dimensions (Conciseness, Aesthetics) only break ties.

## Key Results

| Method | Faithfulness | Conciseness | Readability | Aesthetics | Overall |
|--------|-------------|-------------|-------------|-----------|---------|
| Vanilla Nano-Banana-Pro | 43.0 | 43.5 | 38.5 | 65.5 | 43.0 |
| **PaperBanana** | **45.8** | **80.7** | **51.4** | **72.1** | **60.0** |
| Human Reference | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 |

- PaperBanana beats vanilla by: Faithfulness +2.8%, Conciseness +37.2%, Readability +12.9%, Aesthetics +6.6%, Overall +17.0%
- PaperBanana EXCEEDS human performance in Conciseness and Aesthetics
- Faithfulness remains the hardest dimension (still below human)

## Critical Insights for Implementation

1. **Critique improves accuracy**: Critic Agent raised Faithfulness from ~30.7% (no critic) to 45.8% (3 iterations). Each iteration helps.
2. **Reference examples matter**: Even random references improve output vs. no references. Providing ANY structural examples helps the model learn format and style.
3. **Stylist helps aesthetics but can hurt faithfulness**: Visual polishing sometimes omits technical details. The Critic compensates by recovering accuracy.
4. **"Monkey see, monkey do"**: Showing good examples teaches structure better than describing it. Reference images are more valuable than verbose style instructions.
5. **Narrative descriptions > keyword lists**: Descriptive paragraphs consistently outperform keyword-style prompts for image generation quality.
6. **3 iterations is the sweet spot**: Diminishing returns beyond T=3 Visualizer-Critic rounds.
