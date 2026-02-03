# /dispatch - Multi-Agent Orchestration Command

Dispatch specialized subagents to work on tasks in parallel using **async background agents**, then synthesize results.

**NEW (Dec 2025)**: Uses Claude Code's async background agents for true parallel execution.

## Usage

```
/dispatch                                    # Interactive mode - analyze and recommend
/dispatch task:"Review this PR"              # Specific task with auto-dispatch
/dispatch agents:security,test,docs          # Specific agents for current task
/dispatch pattern:code-review                # Use predefined pattern
/dispatch pattern:codebase-audit scope:src/  # Pattern with scope
/dispatch background:true                    # Force background execution (default)
/dispatch background:false                   # Wait for each agent sequentially
```

## Invocation

When user runs `/dispatch`, activate the orchestrator agent workflow:

### Step 1: Analyze Request

Parse the dispatch request to determine:

```
1. What is the primary goal?
2. Which specialized agents would help?
3. Can tasks run in parallel?
4. What output format is needed?
```

If no specific task provided, analyze recent context:
- Look at last user request
- Check feature_list.json for current work
- Suggest appropriate dispatch pattern

### Step 2: Create Dispatch Plan

Based on analysis, create a dispatch plan:

```markdown
## Dispatch Plan

**Goal**: [Primary objective]
**Pattern**: [code-review | feature-analysis | codebase-audit | custom]

### Agents to Dispatch
| Agent | Focus | Scope | Priority |
|-------|-------|-------|----------|
| security-reviewer | Vulnerabilities | src/api/ | High |
| test-generator | Coverage gaps | src/lib/ | Medium |
| doc-extractor | README updates | . | Low |

### Execution
- Parallel: [agents that can run together]
- Sequential: [agents that depend on others]

### Expected Output
- Combined report with categorized findings
- Priority-ordered action items
```

### Step 3: Dispatch Subagents (Async Background Execution)

**Use `run_in_background: true`** for true parallel execution. All agents run as separate processes:

```
Task tool calls (in single message for parallel dispatch):

1. Task(
     subagent_type: "security-reviewer",
     prompt: "Review src/api/ for security vulnerabilities...",
     run_in_background: true,
     description: "Security audit"
   )

2. Task(
     subagent_type: "test-generator",
     prompt: "Analyze src/lib/ for test coverage gaps...",
     run_in_background: true,
     description: "Test coverage analysis"
   )

3. Task(
     subagent_type: "doc-extractor",
     prompt: "Check if documentation needs updates...",
     run_in_background: true,
     description: "Documentation review"
   )
```

**Key Benefits of Background Execution:**
- True parallel processing (not sequential)
- Each agent has isolated context (no pollution)
- Main agent can continue other work while waiting
- Results collected via `TaskOutput` tool

### Step 3b: Collect Background Results

Use `TaskOutput` to retrieve results from background agents:

```
For each dispatched agent:
  TaskOutput(
    task_id: "<agent_id from dispatch>",
    block: true,  # Wait for completion
    timeout: 60000  # 60 second timeout
  )
```

**Or check status without blocking:**
```
TaskOutput(task_id: "<agent_id>", block: false)
# Returns current status and any output so far
```

### Step 4: Collect and Synthesize Results

As subagents complete, collect outputs and synthesize:

```markdown
## Orchestration Report

**Task**: [Original request]
**Agents**: [list]
**Duration**: [time estimate]

### Summary
[High-level findings across all agents]

### Security Findings
[From security-reviewer]

### Test Recommendations
[From test-generator]

### Documentation Updates
[From doc-extractor]

### Priority Actions
1. [HIGH] [Action from security findings]
2. [MED] [Action from test findings]
3. [LOW] [Action from doc findings]

### Conflicts Resolved
[Any contradictory recommendations]
```

## Available Agents

| Agent | Specialty | Read-Only | Use For |
|-------|-----------|-----------|---------|
| `security-reviewer` | OWASP vulnerabilities | Yes | Security audits |
| `test-generator` | Test cases, coverage | No | Test gaps |
| `doc-extractor` | Documentation | No | README, API docs |
| `ui-validator` | Visual testing | Yes | UI verification |
| `researcher` | Information gathering | Yes | R-P-I Phase 1 |
| `planner` | Blueprint creation | Yes | R-P-I Phase 2 |
| `implementer` | Code execution | No | R-P-I Phase 3 |

## Predefined Patterns

### pattern:code-review
```
Agents: security-reviewer, test-generator, doc-extractor
Scope: Changed files or specified path
Output: Combined review with categorized feedback
```

### pattern:feature-analysis
```
Agents: researcher, security-reviewer, planner
Scope: Feature specification or code area
Output: Implementation plan with security considerations
```

### pattern:codebase-audit
```
Agents: security-reviewer, test-generator, doc-extractor
Scope: Entire src/ directory
Output: Comprehensive health report
```

### pattern:ui-validation
```
Agents: ui-validator, test-generator
Scope: UI pages/components
Output: Visual issues + recommended tests
```

## Resource Guidelines

Based on Anthropic's research on agent scaling:

| Complexity | Agents | Tool Calls Each |
|------------|--------|-----------------|
| Simple | 1-2 | 3-10 |
| Moderate | 2-4 | 10-15 |
| Complex | 4+ | Distributed |

**Rules**:
- Start with fewer agents, scale up if needed
- Each agent should have focused scope
- Avoid overlapping responsibilities
- More agents = more synthesis work

## Token Budget Awareness

**IMPORTANT**: Each background agent consumes significant tokens.

| Agents | Estimated Token Cost |
|--------|---------------------|
| 1 | ~5-10K tokens |
| 2-3 | ~15-30K tokens |
| 4+ | ~40K+ tokens |

**Best Practices**:
- Track token usage when running multiple agents
- Use focused scopes to minimize agent work
- Prefer fewer agents with clear responsibilities
- Consider `/tasks` command to monitor active agents

## Error Handling

**If subagent fails**:
1. Log failure in report
2. Continue with other agents
3. Note incomplete coverage
4. Suggest manual follow-up

**If timeout**:
1. Collect partial results
2. Report what completed
3. Suggest continuing in next dispatch

**If conflicts**:
1. Document both perspectives
2. Apply priority: security > performance > convenience
3. Escalate critical conflicts to user

## Example Sessions

### Example 1: PR Review

```
User: /dispatch task:"Review PR #42"

Claude: Analyzing PR #42...

## Dispatch Plan
**Goal**: Review PR for quality and security
**Pattern**: code-review

### Dispatching 3 agents in parallel...

[After completion]

## Orchestration Report

**Task**: Review PR #42
**Agents**: security-reviewer, test-generator, doc-extractor

### Priority Actions
1. [HIGH] Fix SQL injection in src/api/users.ts:42
2. [MED] Add tests for error handling in UserService
3. [LOW] Update README with new endpoint

Detailed findings below...
```

### Example 2: Feature Analysis

```
User: /dispatch pattern:feature-analysis scope:auth

Claude: Analyzing auth feature area...

## Dispatch Plan
**Goal**: Analyze auth implementation
**Pattern**: feature-analysis

### Dispatching 3 agents...

[Results synthesized with implementation recommendations]
```

## Integration

### With Session Tracking

After dispatch completes:
- Update `claude-progress.txt` with orchestration results
- Update `feature_list.json` if features validated

### With /diary

If significant learnings occurred:
- Capture patterns discovered
- Note architectural insights
- Record agent performance observations

## Output

Report saved to: `./orchestration-report-YYYY-MM-DD.md` (optional)

Quick summary always displayed in chat for immediate action.

---

**Dispatch Command v1.0** | ROK 3.0 Multi-Agent Orchestration
