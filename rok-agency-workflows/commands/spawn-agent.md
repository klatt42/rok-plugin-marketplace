# /spawn-agent - Deploy Specialized Sub-Agent

Deploys specialized agents for parallel or sequential task execution with complexity-aware protocol routing.

**Version**: 2.0 (ROK 3.6-Feynman)

## What This Does

1. **Parses Request**: Identifies agents and deployment mode
2. **Validates Agents**: Confirms agent definitions exist
3. **Assesses Complexity**: Determines protocol depth per agent
4. **Deploys Agents**: Sequential or parallel execution
5. **Aggregates Results**: Synthesizes outputs and learnings

## Usage

```
/spawn-agent [agent-name]
/spawn-agent [agent-name] [agent-name] [agent-name]
/spawn-agent --parallel [agent-name] [agent-name]
/spawn-agent --list
/spawn-agent --create [new-agent-name]
```

## Execution Steps

### 1. Parse Request

```
SPAWN REQUEST
─────────────
Agents requested: [list]
Task context: [current task/problem]
Mode: [sequential | parallel | create]
```

### 2. Validate Agents

```bash
ls ~/.claude/agents/
```

- If exists → Load definition
- If not exists → Offer to create via meta-agent

### 3. Pre-Spawn Complexity Assessment (NEW)

For each agent, assess task complexity BEFORE spawning:

```
PRE-SPAWN ASSESSMENT
────────────────────
Agent: [name]
Task: [what this agent will do]
Complexity: [run /complexity]
Protocol required: [SIMPLE/MEDIUM/COMPLEX]

Spawning [agent-name] with [protocol] protocol...
```

### 4. Deploy Agents

#### Sequential Mode (default)
```
SEQUENTIAL DEPLOYMENT
─────────────────────
Agent 1: [name]
├── Input: [task/context]
├── Protocol: [SIMPLE/MEDIUM/COMPLEX]
├── Output: [expected deliverable]
└── Handoff to: Agent 2

Agent 2: [name]
├── Input: [Agent 1 output]
├── Protocol: [assessed]
├── Output: [expected deliverable]
└── Handoff to: [next or complete]
```

#### Parallel Mode
```
PARALLEL DEPLOYMENT
───────────────────
Spawning simultaneously:

┌─ Agent A: [name]
│  Task: [specific focus]
│  Protocol: [assessed]
│
├─ Agent B: [name]
│  Task: [specific focus]
│  Protocol: [assessed]
│
└─ Agent C: [name]
   Task: [specific focus]
   Protocol: [assessed]

Aggregation: [how results will be combined]
```

### 5. Execute Agent Workflows

Each agent follows its defined workflow from `~/.claude/agents/[name].md`:

```
AGENT EXECUTION: [name]
══════════════════════

[Agent performs its defined workflow]

OUTPUT:
───────
[Agent's deliverable]

LEARNINGS:
──────────
[Any assumption-corrections or patterns discovered]
```

### 6. Aggregate Results

```
═══════════════════════════════════════════════════════
SPAWN RESULTS AGGREGATION
═══════════════════════════════════════════════════════

Agents deployed: [list]
Mode: [sequential/parallel]

INDIVIDUAL OUTPUTS:
───────────────────
Agent [A]: [summary]
Agent [B]: [summary]
Agent [C]: [summary]

SYNTHESIS:
──────────
[Combined insights, resolved conflicts, unified recommendation]

CONFLICTS/TENSIONS:
───────────────────
[Where agents disagreed - valuable for decision-making]

COLLECTIVE LEARNINGS:
─────────────────────
[Aggregated assumption-corrections and patterns]

═══════════════════════════════════════════════════════
```

### 7. Learning Capture

- Collect assumption-corrections from each agent
- Identify cross-cutting patterns
- Flag for session /diary

## Available Agents

```
/spawn-agent --list
```

```
AVAILABLE AGENTS
────────────────
~/.claude/agents/

Core Agents (ROK 3.6-Feynman):
  • meta-agent     - Creates/coordinates agents (N/A complexity)
  • researcher     - Gathers information (MEDIUM default)
  • planner        - Creates blueprints (COMPLEX always)
  • implementer    - Executes plans (per-step assessment)

Specialized Agents:
  • orchestrator       - Multi-agent coordination (COMPLEX)
  • security-reviewer  - OWASP vulnerability detection (COMPLEX)
  • test-generator     - Test case generation (MEDIUM)
  • doc-extractor      - Documentation extraction (SIMPLE)
  • ui-validator       - Visual UI validation (MEDIUM)

To create new agent:
  /spawn-agent --create [name]
```

## Multi-Agent Patterns

### Pattern 1: Research Triangulation
```
/spawn-agent researcher researcher researcher
```
Three researchers examine from different angles.

### Pattern 2: Security Review Pipeline
```
/spawn-agent researcher security-reviewer planner implementer
```
Sequential with security checkpoint.

### Pattern 3: Multi-Perspective Analysis
```
/spawn-agent --parallel security-reviewer test-generator doc-extractor
```
Parallel review, then synthesize.

### Pattern 4: R-P-I Full Flow
```
/spawn-agent researcher
# Review research output
/spawn-agent planner
# Approve plan
/spawn-agent implementer
```

### Pattern 5: Iterative Refinement
```
/spawn-agent implementer
# Test fails
/spawn-agent implementer
# Repeat until passing
```

## Creating New Agents

```
/spawn-agent --create api-integration-specialist
```

Triggers meta-agent to:
1. Analyze capabilities needed
2. Generate agent definition with complexity_default
3. Save to `~/.claude/agents/[name].md`
4. Report availability

## Output Locations

| Agent Type | Output Location |
|------------|-----------------|
| Researcher | `thoughts/shared/research/` |
| Planner | `thoughts/shared/plans/` |
| Implementer | `thoughts/shared/expertise/` (learnings) |
| Aggregation | `thoughts/shared/agents/spawn-synthesis.md` |

## Integration with R-P-I

```bash
# Phase 1: Research
/1_research <feature>
# or
/spawn-agent researcher <feature>

# Phase 2: Plan
/2_plan thoughts/shared/research/[feature]-research.md
# or
/spawn-agent planner <research-file>

# Phase 3: Implement (after approval)
/3_implement thoughts/shared/plans/[feature]-plan.md
# or
/spawn-agent implementer <plan-file>
```

## Tips

- Check complexity assessment before complex deployments
- Spawn multiple researchers for comprehensive coverage
- Always synthesize multi-agent outputs
- Use parallel mode for independent analyses
- Sequential mode when outputs feed into next agent

---

**Spawn-Agent Command v2.0** | ROK 3.6-Feynman Complexity-Aware Routing
