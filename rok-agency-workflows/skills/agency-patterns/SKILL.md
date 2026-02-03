---
name: agency-patterns
description: |
  Agency workflow patterns for managing multiple client projects, multi-agent
  orchestration, cross-project memory, and browser-based UI validation.
  Includes dispatch for parallel agent work, spawn-agent for specialized
  delegation, and memory system for persistent context.
triggers:
  - "client project"
  - "agency workflow"
  - "multi-agent"
  - "dispatch agents"
  - "project management"
  - "validate UI"
version: 1.0
author: ROK Copilot
---

# Agency Patterns

## Multi-Agent Orchestration

### /dispatch - Parallel Agent Work
- Spawn multiple specialized agents for read-only analysis
- Each agent focuses on one aspect (security, performance, architecture)
- Results aggregated and synthesized

### /spawn-agent - Task Delegation
- Create specialized sub-agents for specific tasks
- Agent types: researcher, implementer, security-reviewer, test-generator
- Full context inheritance from parent

## Memory System

### /memory-write - Persist Context
- Categories: decision, pattern, gotcha, preference
- Stored in Supabase for cross-session persistence
- Synced via /sync-context

### /memory-query - Retrieve Context
- Query by category, key, or full-text search
- Use --synthesize for AI-powered summaries
- Cross-project context retrieval

## UI Validation

### /validate-ui - Browser Testing
- Launch Chrome automation for visual validation
- Compare screenshots against expectations
- Accessibility and responsive checks

## PRD & Feature Management

### /create-prd - Generate Requirements
- Structured product requirements documents
- Stakeholder analysis, success metrics, technical constraints

### /generate-feature-list - Track Features
- Create structured feature tracking JSON
- Status tracking, priority ordering, dependency mapping
