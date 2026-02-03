# ROK 2.0 Clean Context Session Initialization

Initializes a fresh ROK 2.0 session with full knowledge preservation and context recovery.

## What This Does

1. **Loads ROK 2.0 System**: Establishes knowledge preservation framework
2. **Shows Available Projects**: Lists all 6 documented projects
3. **Loads Project Context**: Retrieves CLAUDE.md from /tmp/ for selected project
4. **Initializes Session Tracking**: Prepares for work and progress tracking
5. **Token Budget Setup**: Establishes 200K token budget awareness
6. **Ready for Development**: Full context loaded in 5-10 minutes

## Usage

In Claude (Code or Desktop):
```
/rok-clean-session
```

## Session Initialization Process

### Step 1: ROK 2.0 System Load
- Load `/home/klatt42/.claude/CLAUDE.md` for ROK system reference
- Confirm token budget: 200,000 tokens available
- Display ROK 2.0 advancements (December 2025)

### Step 2: Project Selection
Display available projects:
```
Select a project to load:
1. SERP-Master (B2B Lead Generation Engine)
2. Prism DMV (Specialty Restoration Landing Page)
3. BizInsiderPro (AI Consulting Landing Page)
4. NicheLead AI Engine (B2B Lead Generation Platform)
5. Project Genesis (AI Skills Framework)
6. AMPLIFY ENGINE (Content Intelligence Architect)
7. [Other project not listed]
```

### Step 3: Context Load
Once project selected:
- Load main CLAUDE.md from /tmp/ (1000+ lines, 5-10 min read)
- Display quick reference from QUICK_REFERENCE.txt
- Show architecture decisions summary
- Display latest session summary and status

### Step 4: Development Readiness Check
```
✅ ROK 2.0 Session Ready

Project: [SELECTED PROJECT]
Context Loaded: [CLAUDE.md + architecture-decisions.md]
Status: [Current development phase]
Next Steps: [From session-summary.md]
Token Budget: 200,000 available (~150K for work)

Ready to begin development. Use normal workflow:
- /plan [feature description] - Plan work
- /build [implementation] - Build features
- Ask for code reviews, tests, etc.

Session will auto-track:
- Work accomplished
- Code changes
- Design decisions
- Issues and blockers
```

### Step 5: Session Work
During the session:
- Develop normally on selected project
- Make commits with ROK conventions: `[ROK] Feature: description`
- Track accomplished work
- Note blockers and decisions

### Step 6: Session Completion (Manual)
Before ending session:

1. **Commit Work**:
```bash
git add .
git commit -m "[ROK] Session complete: [feature] implementation

- Accomplished: [what was done]
- In progress: [what's next]
- Blockers: [any issues]

🤖 Generated with Claude Code + ROK 2.0
Co-Authored-By: Claude <noreply@anthropic.com>"
```

2. **Update Session Summary**:
- Review /tmp/[project]-session-summary-2025-12-06.md
- Add today's work to accomplishments
- Update roadmap and next steps
- Save updated summary

3. **Verify Knowledge Preserved**:
- Confirm /tmp/ files exist for project
- Check CLAUDE.md has latest architecture
- Verify quick reference is accurate
- Ensure session-summary.md updated

4. **Ready for Next Session**:
- All context preserved in /tmp/
- Can resume in 5-10 minutes next time
- Safe to compact if needed
- Knowledge persists indefinitely

## Token Budget Monitoring

**Budget**: 200,000 tokens per session

**Typical Allocation**:
- ROK 2.0 system context: 2-4K tokens
- Project CLAUDE.md load: 8-12K tokens
- Active development work: 50-100K tokens
- Buffer for complex tasks: 50-100K tokens
- **Available for development**: ~150K tokens

**Compaction Trigger**:
- When reaching 150K tokens used
- Compaction reclaims 15K+ tokens
- Safe because all knowledge in /tmp/

## Directory Structure Reference

```
/home/klatt42/                           # WSL home directory
├── projects/                            # All active projects
│   ├── amplify-engine/
│   ├── bizinsiderpro/
│   ├── nichelead-ai-engine/
│   ├── project-genesis/
│   └── remote-agentic-coding-clean/
│       └── workspace/
│           ├── serp-master/
│           └── prism-specialties-dmv-empire/
├── .claude/
│   ├── CLAUDE.md                        # ROK 2.0 system reference (this)
│   ├── commands/
│   │   └── rok-clean-session.md         # This file
│   └── skills/
└── [other config directories]

/tmp/                                    # Knowledge preservation storage
├── AmplifyEngine_CLAUDE.md              # Project context
├── amplify-engine-architecture-decisions.md
├── amplify-engine-session-summary-2025-12-06.md
├── AMPLIFYENGINE_QUICK_REFERENCE.txt
└── [Similar for other 5 projects]
```

## Quick Start Alternatives

### Option 1: Slash Command (Recommended)
```
In Claude: /rok-clean-session
Select project → Context loads → Ready to work
```

### Option 2: Manual Context Load
```bash
# From WSL terminal
cd /home/klatt42
cat /tmp/AmplifyEngine_CLAUDE.md | less
cd projects/amplify-engine
npm run dev
```

### Option 3: Using Aliases
```bash
# Add to ~/.bashrc (one time)
alias rok-amplify='cd ~/projects/amplify-engine'

# Use in WSL
rok-amplify
cat /tmp/AmplifyEngine_CLAUDE.md
npm run dev
```

## Session Handoff Protocol

### For Continuing Sessions (Same Day)
- Load project again: `/rok-clean-session`
- Select same project
- Context preserved from last session
- Continue where you left off

### For Next-Day Sessions (New Context)
- ROK 2.0 system: Auto-loads from `/home/klatt42/.claude/CLAUDE.md`
- Project context: Auto-loads from `/tmp/PROJECT_CLAUDE.md` (5-10 min)
- No manual recovery needed
- All knowledge preserved across compactions

### For Context Compaction (Safe!)
- All knowledge preserved in /tmp/ files
- Can safely compact main context
- Next session recovers in 5-10 minutes
- No knowledge loss

## Session Examples

### Example 1: Building AMPLIFY ENGINE CM-003
```
User: /rok-clean-session
Claude: Shows 6 projects
User: Selects AMPLIFY ENGINE (option 6)
Claude: Loads 1000+ lines from /tmp/AmplifyEngine_CLAUDE.md
        Shows status: "CM-003 Content Intelligence Architect - In Progress"
        Displays: "Phase 1: Agent coordination implementation"

User: "Let's implement the viral potential scoring algorithm"
Claude: [Development begins with full context]
        Understands: BMAD agents, Authority Reversal Framework, tech stack
        Can: Generate code matching existing patterns
        Tracks: Work accomplished this session

End of Session:
- Commit: [ROK] CM-003: Implement viral potential scoring
- Update: /tmp/amplify-engine-session-summary-2025-12-06.md
- Ready: Next session resumes instantly
```

### Example 2: Switching Between Projects
```
Morning Session:
/rok-clean-session → Select AMPLIFY ENGINE → Work
[End session, commit, update summary]

Afternoon Session:
/rok-clean-session → Select NicheLead → Work
[Full context loads for different project]
[No manual context switching needed]
```

### Example 3: After Context Compaction
```
Previous Session: Full context ~140K tokens
Compaction: Reduced to ~4K tokens
Next Session:
/rok-clean-session → Select AMPLIFY ENGINE
Claude: Loads /tmp/AmplifyEngine_CLAUDE.md
        Instantly recovers all architecture knowledge
        No information lost despite compaction
        Ready to continue development
```

## Troubleshooting

### Context Files Missing
If `/tmp/` files not found:
```bash
# Check file existence
ls /tmp/*CLAUDE.md | head

# If missing, re-create:
# Load full CLAUDE.md from project directory
cat ~/projects/amplify-engine/CLAUDE.md > /tmp/AmplifyEngine_CLAUDE.md
```

### Token Budget Questions
"How many tokens have I used so far?"
Claude will show current usage and remaining budget.

### Project Not Listed
If desired project not in selection:
```bash
# Manually specify project
cd /home/klatt42/projects/[project-name]
cat /tmp/[PROJECT]_CLAUDE.md | less
```

### Compaction Safety Check
```bash
# Verify all knowledge preserved before compacting
ls -1 /tmp/*CLAUDE.md /tmp/*QUICK_REFERENCE.txt | wc -l
# Should show 23 files for all 6 projects
```

## Success Criteria

After running `/rok-clean-session`, you should be able to:

- [ ] Identify the ROK 2.0 system and its benefits
- [ ] Select a project from the list
- [ ] Load full context in 5-10 minutes
- [ ] Understand project status from session summary
- [ ] Access architecture decisions and design rationale
- [ ] Begin development with full knowledge
- [ ] Track work during the session
- [ ] Commit with ROK conventions
- [ ] Update session summary
- [ ] Prepare for next session

---

**Status**: ROK 2.0 Clean Context Session Ready ✅

Use this command to initialize any development session with full knowledge preservation and instant context recovery.

Start with: `/rok-clean-session`
