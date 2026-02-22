# /generate-snapshot - Generate Digital Estate Snapshot

Generate a comprehensive digital estate snapshot for bus factor mitigation and work continuity. Scans local projects, GitHub repos, Netlify/Vercel deployments, ROK Supabase memory, and manual infrastructure config. Produces a 10-section document with urgency-scored items.

## Usage

```
/rok-digital-estate:generate-snapshot                      # Full snapshot (all 5 sources)
/rok-digital-estate:generate-snapshot refresh               # Force regeneration
/rok-digital-estate:generate-snapshot source:local          # Local projects only
/rok-digital-estate:generate-snapshot source:github         # GitHub repos only
/rok-digital-estate:generate-snapshot source:deployments    # Deployments only
/rok-digital-estate:generate-snapshot source:infrastructure # Infrastructure only
/rok-digital-estate:generate-snapshot source:memory         # ROK memory only
```

### Parameters
- **refresh** - Force regeneration even if a recent snapshot exists
- **source** - Limit to a specific data source (default: all)

### Output Folder
All exported files (MD, HTML, PDF) are written to:
```
~/projects/rok-copilot/estate-snapshots/
```

Initial request: $ARGUMENTS

## Execution Steps

### Phase 1: Check Current State

1. **Check for existing snapshot**:
   ```bash
   ls ~/projects/rok-copilot/estate-snapshots/*_estate-snapshot_v*.md 2>/dev/null | sort -V | tail -1
   ```

   Extract version number from filename pattern `*_estate-snapshot_v[N].*`. The new snapshot will be current + 1. If no files found, this is version 1.

2. Parse existing state:
   - If a snapshot exists and `refresh` is NOT in $ARGUMENTS:
     - Check file modification time
     - If less than 24 hours old: display summary and ask "This snapshot is [X hours] old. Refresh? (yes/no)"
     - If older than 24 hours: note "Snapshot is [X days] old" and proceed to Phase 2
   - If no snapshot exists, proceed to Phase 2

3. If `refresh` IS in $ARGUMENTS, always proceed to Phase 2

Display:
```
SNAPSHOT STATUS
Latest Version: v[N] (generated [date])
Status: [Current / Stale / None]
```

### Phase 2: Prerequisites Check

1. **Verify estate-config.json exists**:
   ```bash
   test -f ~/projects/rok-copilot/estate-snapshots/estate-config.json && echo "CONFIG_FOUND" || echo "CONFIG_MISSING"
   ```

   If missing, warn but continue:
   ```
   WARNING: estate-config.json not found.
   Infrastructure data (domains, subscriptions, contacts) will be incomplete.
   To create: copy reference/estate-config-example.json to ~/projects/rok-copilot/estate-snapshots/estate-config.json
   ```

2. **Verify gh CLI is authenticated**:
   ```bash
   gh auth status 2>&1 | head -3
   ```

3. **Verify Supabase env vars**:
   ```bash
   test -n "${ROK_SUPABASE_URL}" && echo "SUPABASE_URL_SET" || echo "SUPABASE_URL_MISSING"
   test -n "${ROK_SUPABASE_KEY}" && echo "SUPABASE_KEY_SET" || echo "SUPABASE_KEY_MISSING"
   ```

4. **Create output directory**:
   ```bash
   mkdir -p ~/projects/rok-copilot/estate-snapshots/
   ```

Display:
```
PREREQUISITES
Config file: [Found / Missing]
GitHub CLI: [Authenticated / Not available]
Supabase: [Connected / Not configured]
Output dir: [Ready]
```

### Phase 3: Parallel Agent Dispatch (5 Agents)

If `source:` parameter limits the scan, only dispatch the relevant agent(s). Otherwise dispatch all 5 in parallel.

1. **Load previous snapshot** (if exists) for delta detection:
   ```bash
   PREV_FILE=$(ls ~/projects/rok-copilot/estate-snapshots/*_estate-snapshot_v*.md 2>/dev/null | sort -V | tail -1)
   ```
   Read this file's content for passing to the synthesizer.

2. **Dispatch local-scanner** agent (background):
   ```
   Task(
     subagent_type: "local-scanner",
     description: "Scan local projects for estate snapshot",
     prompt: "You are the local-scanner agent. [Include agent instructions from agents/local-scanner.md]

     Scan ~/projects/ and classify all projects. Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

3. **Dispatch github-analyst** agent (background):
   ```
   Task(
     subagent_type: "github-analyst",
     description: "Scan GitHub repos for estate snapshot",
     prompt: "You are the github-analyst agent. [Include agent instructions from agents/github-analyst.md]

     Query all GitHub repos via gh CLI. Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

4. **Dispatch deployment-analyst** agent (background):
   ```
   Task(
     subagent_type: "deployment-analyst",
     description: "Scan deployments for estate snapshot",
     prompt: "You are the deployment-analyst agent. [Include agent instructions from agents/deployment-analyst.md]

     Query Netlify and Vercel for all deployments. Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

5. **Dispatch infrastructure-analyst** agent (background):
   ```
   Task(
     subagent_type: "infrastructure-analyst",
     description: "Analyze infrastructure for estate snapshot",
     prompt: "You are the infrastructure-analyst agent. [Include agent instructions from agents/infrastructure-analyst.md]

     Read estate-config.json and process infrastructure data. Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

6. **Dispatch memory-analyst** agent (background):
   ```
   Task(
     subagent_type: "memory-analyst",
     description: "Query ROK memory for estate snapshot",
     prompt: "You are the memory-analyst agent. [Include agent instructions from agents/memory-analyst.md]

     Query Supabase for institutional knowledge. Return structured JSON per your output format.",
     run_in_background: true
   )
   ```

7. **Collect results** from all agents via TaskOutput (block: true):
   ```
   TaskOutput(task_id: "<local_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<github_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<deployment_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<infrastructure_task_id>", block: true, timeout: 120000)
   TaskOutput(task_id: "<memory_task_id>", block: true, timeout: 120000)
   ```

Display:
```
AGENT RESULTS
Local Scanner: [Complete / Partial / Failed]
GitHub Analyst: [Complete / Partial / Failed]
Deployment Analyst: [Complete / Partial / Failed]
Infrastructure Analyst: [Complete / Partial / Failed]
Memory Analyst: [Complete / Partial / Failed]
```

### Phase 4: Master Synthesis

1. **Validate agent outputs**: For each agent result, attempt JSON parsing:
   - Try direct JSON parse
   - If that fails, extract from markdown code fence
   - If that fails, note partial data and continue

2. **Dispatch estate-synthesizer** agent:
   ```
   Task(
     subagent_type: "estate-synthesizer",
     description: "Synthesize estate snapshot document",
     prompt: "You are the estate-synthesizer agent. [Include agent instructions from agents/estate-synthesizer.md]

     LOCAL SCANNER OUTPUT:
     [JSON from local-scanner]

     GITHUB ANALYST OUTPUT:
     [JSON from github-analyst]

     DEPLOYMENT ANALYST OUTPUT:
     [JSON from deployment-analyst]

     INFRASTRUCTURE ANALYST OUTPUT:
     [JSON from infrastructure-analyst]

     MEMORY ANALYST OUTPUT:
     [JSON from memory-analyst]

     PREVIOUS SNAPSHOT:
     [Previous full_estate_md, or 'This is the first estate snapshot']

     SNAPSHOT VERSION: v[N]
     SNAPSHOT DATE: [today YYYY-MM-DD]

     Synthesize all data into a complete estate document. Return structured JSON per your output format.",
     run_in_background: false
   )
   ```

3. Parse the synthesizer's JSON response

### Phase 5: Export and Store

1. **Determine version number**: Previous version + 1, or 1 if first snapshot.

2. **Write export JSON** to temp file:
   ```bash
   cat > /tmp/estate_snapshot_export.json << 'EXPORT_EOF'
   [synthesizer JSON output]
   EXPORT_EOF
   ```

3. **Execute export script**:
   ```bash
   ~/.claude/scripts/.venv/bin/python3 \
     ~/.claude/plugins/marketplaces/rok-plugin-marketplace/rok-digital-estate/scripts/estate_snapshot_export.py \
     --input /tmp/estate_snapshot_export.json \
     --output-dir ~/projects/rok-copilot/estate-snapshots/
   ```

4. **Clean up temp file**:
   ```bash
   rm -f /tmp/estate_snapshot_export.json
   ```

5. **Display results**:
   ```
   =========================================
   ESTATE SNAPSHOT COMPLETE
   =========================================
   Version: v[N]
   Estate Health: [HEALTHY / NEEDS ATTENTION / CRITICAL ITEMS]
   Projects: [count] | Deployments: [count]
   Monthly Burn: $[total]
   Critical Items: [count]
   Completeness: [score]%

   Generated Files:
     MD:   [filename].md
     HTML: [filename].html
     PDF:  [filename].pdf

   Output Folder: ~/projects/rok-copilot/estate-snapshots/
   =========================================
   ```

6. **Display the full estate document** (render `full_estate_md`)

## Important Rules

- For `refresh`, always regenerate even if a recent snapshot exists
- For `source:` filter, only dispatch the specified agent but still run the synthesizer with partial data
- Graceful degradation: if any agent fails, continue with available data and note gaps
- NEVER include actual passwords, API keys, or tokens in any output
- The synthesizer uses the opus model for highest quality synthesis
- Always preserve previous snapshots -- never overwrite, only create new versions
- If an agent fails or times out (120s), proceed with the others and note the gap
- Clean up `/tmp/estate_snapshot_export.json` after export, even on failure
- The Bus Factor Dashboard is the most critical section -- ensure urgency items are always present
