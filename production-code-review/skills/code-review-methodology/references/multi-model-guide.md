# Multi-Model Code Review Guide

## Overview

The production-code-review plugin v2.0 supports reviewing code with up to 3 AI models in parallel: Claude Code (subagents), OpenAI Codex CLI, and Google Gemini CLI. This guide explains the architecture and troubleshooting.

## Mode Selection

| Mode | Models | Use When |
|------|--------|----------|
| `single/claude` | Claude only (6 subagents) | Default, fastest within Claude context |
| `single/codex` | Codex CLI only | Want OpenAI's code review perspective |
| `single/gemini` | Gemini CLI only | Want Google's code review perspective |
| `multi` | All 3 in parallel | Pre-production, thorough review needed |

## CLI Requirements

| CLI | Install | Auth |
|-----|---------|------|
| Codex | `npm install -g @openai/codex` | `codex login` |
| Gemini | `npm install -g @anthropic-ai/gemini-cli` (or via Google) | `gemini auth login` |

## Consensus Scoring

When multiple models find the same issue (same file, line within +/-5):
- **3/3 models agree**: Highest confidence, listed first in recommendations
- **2/3 models agree**: High confidence, confidence boosted +5
- **1/3 unique finding**: Original confidence, tagged as unique (still included)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Codex: "authentication error" | Run `codex login` |
| Gemini: "credentials" error | Run `gemini auth login` |
| Codex timeout | Increase timeout or reduce project scope |
| Gemini output not JSON | Known issue with some models; parser attempts extraction |
| External CLI not found | Install via npm; multi-model degrades gracefully |

## Token Costs

- Claude: charged to your Anthropic account (~60-90K per review)
- Codex: charged to your OpenAI account
- Gemini: charged to your Google account
- Multi-model total: sum of all three (external costs are independent)
