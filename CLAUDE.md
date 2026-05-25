# CLAUDE.md: Claude Workflow for Roblox Tower Defense Prototype

## Overview

This document defines how Claude integrates with the Roblox Tower Defense prototype development workflow.

**Current Status:** Claude is the primary development agent (Codex CLI pending)

**Project-Local Skills:** New `.claude/skills/` directory contains specialized skills for this project:
- `roblox-demo-pipeline/SKILL.md` — Demo automation, video recording, marker collection
- `token-saver-code-agent/SKILL.md` — Token optimization, efficient file reading
- `safe-git-review/SKILL.md` — Pre-commit review, file classification, safe staging

**Project-Local Commands:** New `.claude/commands/` directory contains quick-start commands:
- `continue-demo.md` — Resume demo/video verification pipeline
- `precommit-review.md` — Pre-commit safety review before staging

---

## Core Workflow: Plan → Implement → Test → Merge

### 1. Plan Mode (Architect Role)

**When to use:**
- Starting a new feature
- Analyzing codebase changes
- Designing system architecture
- Evaluating technical risks

**Process:**
1. Read `docs/team/CURRENT_STATE.md` and `docs/team/ROADMAP.md`
2. Use `prompts/audit_codebase.md` to understand existing code
3. Use `prompts/design_feature.md` to create detailed design
4. Create plan file at `C:\Users\Bogdan\.claude\plans\<name>.md`
5. Ask user for approval before implementation
6. **Do NOT modify files** until plan is approved

**Key constraint:** Plan mode is read-only. Use tools to explore, but do not edit files.

**Example:**
```
User: "Add tower placement spending system"
Claude: 
  1. Reads EconomyService, TowerService, TowerConfig
  2. Creates plan with design, affected files, verification steps
  3. Writes plan to .claude/plans/
  4. Asks user for approval
```

---

### 2. Implementation Mode (Developer Role)

**When to use:**
- After plan approval
- Building new features
- Fixing bugs
- Adding tests

**Process:**
1. Read approved plan file
2. Use `prompts/implement_code.md` for guidance
3. Make minimal, focused edits using `edit` tool
4. Follow existing code patterns and style
5. Add necessary imports and dependencies
6. Create PR with clear description
7. Handoff to testing phase

**Key constraint:** Implement only what the plan specifies. No scope creep.

**Example:**
```
User: "Plan approved, implement tower placement spending"
Claude:
  1. Edits TowerService.lua to add spending logic
  2. Updates TowerConfig.lua with costs
  3. Edits EconomyService.lua to deduct money
  4. Runs build_place.ps1 to verify
  5. Creates PR with description
```

---

### 3. Testing Mode (Tester Role)

**When to use:**
- After PR is created
- Before merge
- Verifying game logic
- Collecting evidence

**Process:**
1. Run `team_review_demo.ps1` to execute demo
2. Use `prompts/test_game.md` to verify features
3. Collect logs, screenshots, video
4. Analyze Roblox Output logs
5. Create test report
6. Approve or request changes

**Key constraint:** Use safe Studio Operator flows. Do not manually modify Studio.

**Example:**
```
User: "Test the tower placement spending PR"
Claude:
  1. Runs team_review_demo.ps1
  2. Checks logs/demo_test_report.md
  3. Verifies money deducted when tower placed
  4. Verifies tower not placed if insufficient funds
  5. Approves or requests changes
```

---

### 4. Merge Mode (DevOps Role)

**When to use:**
- After testing passes
- All checks verified
- Ready to integrate

**Process:**
1. Verify working tree is clean: `git status`
2. Run `pr_safe_merge.ps1 -PrNumber <N>`
3. Verify merge succeeds
4. Update `docs/team/CURRENT_STATE.md`
5. Commit state update
6. Handoff to next feature

**Key constraint:** Use safe merge scripts. Never force push.

**Example:**
```
User: "Merge the tower spending PR"
Claude:
  1. Runs pr_safe_merge.ps1 -PrNumber 9
  2. Verifies all checks pass
  3. Updates CURRENT_STATE.md
  4. Commits with clear message
  5. Confirms merge complete
```

---

## Model Routing for Claude

Claude should use appropriate models based on task complexity:

### Quick Tasks (Use `/model haiku`)
- Documentation updates
- Status checks
- Simple scripts
- Summarization
- Prompt library management

**Command:**
```
/model haiku
```

### Code Tasks (Use `/model sonnet`)
- Feature implementation
- Bug fixes
- Code review
- Test writing
- Single-service changes

**Command:**
```
/model sonnet
```

### Deep Tasks (Use `/model opusplan` or `/model opus`)
- Architecture design
- Complex debugging
- Cross-service refactoring
- Security reviews
- Risky operations (merge, PR manager)

**Command:**
```
/model opusplan
```

Or if opusplan unavailable:
```
/model opus
```

### Starting New Sessions

To start a new Claude session with specific model:

```powershell
# Quick model
claude --model haiku

# Code model
claude --model sonnet

# Deep model
claude --model opusplan
```

### Switching Models Mid-Task

If task complexity increases:

```
/model opusplan
```

### Model Selection Rules
- ❌ Never use haiku for risky merge/security/hard architecture
- ✅ Always use opusplan for architecture and security
- ✅ Use sonnet for normal code work
- ✅ Use haiku for documentation and status

### Getting Recommendations

To get model recommendation for a task:

```powershell
.\scripts\model_recommend.ps1 -Task "your task description"
```

Examples:
```powershell
.\scripts\model_recommend.ps1 -Task "update README"
.\scripts\model_recommend.ps1 -Task "add tower placement spending"
.\scripts\model_recommend.ps1 -Task "fix PR safe merge manager bug"
```

---

### Prompt Location
All prompts are in `prompts/` directory:
```
prompts/
├── system_base.md           # Base system prompt
├── audit_codebase.md        # Analyze code
├── design_feature.md        # Design new feature
├── implement_code.md        # Implement code
├── review_pr.md             # Review PR
├── test_game.md             # Test game
├── team_status.md           # Check team status
└── team_plan.md             # Plan next tasks
```

### How to Use Prompts

1. **View available prompts:**
   ```powershell
   .\scripts\prompt_list.ps1
   ```

2. **Read a specific prompt:**
   ```powershell
   .\scripts\prompt_show.ps1 -Name design_feature
   ```

3. **Apply prompt in Claude:**
   - Copy prompt content
   - Paste into Claude chat
   - Provide context (files, requirements)
   - Follow prompt guidance

### Prompt Adaptation

Prompts are templates, not rigid rules. Adapt them to:
- Specific feature requirements
- Current codebase state
- Team constraints
- Time availability

---

## File Editing Best Practices

### Before Editing
1. Read the file with `read_file` tool
2. Understand existing patterns
3. Identify where changes go
4. Plan minimal edits

### During Editing
1. Use `edit` tool for focused changes
2. Preserve indentation and style
3. Keep edits small and atomic
4. Add imports at top of file

### After Editing
1. Verify syntax (run build if applicable)
2. Check for regressions
3. Test the change
4. Document in PR description

### Example: Adding a Config Value
```
1. Read: src/shared/configs/TowerConfig.lua
2. Identify: where to add new property
3. Edit: add property with correct format
4. Verify: build_place.ps1 succeeds
5. Test: game loads and uses new value
```

---

## Git & PR Workflow

### Creating a PR

1. **Ensure clean tree:**
   ```bash
   git status
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/tower-spending
   ```

3. **Make changes and commit:**
   ```bash
   git add src/
   git commit -m "Add tower placement spending system"
   ```

4. **Push branch:**
   ```bash
   git push origin feature/tower-spending
   ```

5. **Create PR via gh:**
   ```bash
   gh pr create --title "Add tower placement spending" --body "..."
   ```

### Merging a PR

**Always use safe merge:**
```powershell
.\scripts\pr_safe_merge.ps1 -PrNumber 9
```

**Never force push:**
```bash
git push --force  # ❌ DO NOT DO THIS
```

---

## Team Orchestrator Integration

### Check Team Status
```powershell
.\scripts\team_status.ps1
```

Output includes:
- Current branch and commits
- Open PRs
- Game state (features, services)
- Recent test results

### Plan Next Tasks
```powershell
.\scripts\team_plan_next.ps1
```

Output includes:
- Suggested next features
- Priority ranking
- Estimated effort
- Dependencies

### Review Demo
```powershell
.\scripts\team_review_demo.ps1
```

Output includes:
- Demo test report
- Video recording
- Screenshots
- Roblox logs

### Full Cycle
```powershell
.\scripts\team_cycle.ps1
```

Executes:
1. Status check
2. Plan next tasks
3. Dry run (build without Studio)
4. Demo test
5. Report generation

---

## Documentation Structure

### Team Knowledge Base
```
docs/team/
├── ROLES.md                 # Team member roles
├── ROADMAP.md              # 6-month feature roadmap
├── DEVELOPMENT_LOOP.md     # Standard dev cycle
├── TEST_PLAN.md            # Testing strategy
├── CURRENT_STATE.md        # Current game state
└── NEXT_ACTIONS.md         # Next 3-5 tasks
```

### How to Use
- **Before starting:** Read `CURRENT_STATE.md` and `ROADMAP.md`
- **During planning:** Reference `DEVELOPMENT_LOOP.md`
- **During testing:** Use `TEST_PLAN.md` checklist
- **After merge:** Update `CURRENT_STATE.md`

---

## Safety Rules (Claude-Specific)

### Always Do
- ✅ Read files before editing
- ✅ Use plan mode for complex features
- ✅ Test changes before merge
- ✅ Use safe merge scripts
- ✅ Keep working tree clean
- ✅ Document changes in PRs

### Never Do
- ❌ Edit files without reading first
- ❌ Commit build/ or logs/
- ❌ Add secrets or tokens
- ❌ Force push
- ❌ Merge without testing
- ❌ Modify game code without plan approval

### If Uncertain
- Ask user for clarification
- Read relevant documentation
- Run verification scripts
- Check existing patterns in codebase

---

## Common Tasks

### Add a New Game Feature
1. Plan mode: Design feature with `design_feature.md`
2. Implementation: Code in `src/` following patterns
3. Testing: Run `team_review_demo.ps1`
4. Merge: Use `pr_safe_merge.ps1`

### Fix a Bug
1. Identify bug location
2. Read relevant code
3. Make minimal fix
4. Test with demo
5. Merge with safe script

### Update Documentation
1. Read existing docs
2. Identify what needs updating
3. Edit `.md` files
4. Verify links and formatting
5. Commit with clear message

### Review a PR
1. Read PR description
2. Check changed files
3. Verify against `TEST_PLAN.md`
4. Run demo if game code changed
5. Approve or request changes

---

## Troubleshooting

### Build Fails
```powershell
.\scripts\build_place.ps1
# Check error output
# Verify Rojo is installed: rojo --version
# Check default.project.json syntax
```

### Studio Won't Focus
```powershell
.\scripts\auto_play_assisted.ps1
# Manually click Studio window when prompted
# F5 will be sent after focus confirmed
```

### Demo Test Blocked
```powershell
.\scripts\team_review_demo.ps1
# Check logs/demo_test_report.md
# Verify Studio is not already open
# Check process state: .\scripts\operator_status.ps1
```

### PR Merge Fails
```powershell
.\scripts\pr_status.ps1
# Check PR status and checks
# Verify working tree is clean
# Verify gh auth is active: gh auth status
```

---

## Integration with Codex CLI

When Codex CLI becomes available:

1. **Codex agents** will follow `AGENTS.md` roles
2. **Claude** will continue using this workflow
3. **Handoffs** will use team_orchestrator.py
4. **Prompts** will be shared between Claude and Codex

No changes needed to this workflow when Codex CLI launches.

---

## Quick Reference

| Task | Command | Role |
|------|---------|------|
| Check status | `team_status.ps1` | DevOps |
| Plan feature | Create plan file | Architect |
| Implement | Edit `src/` files | Developer |
| Test | `team_review_demo.ps1` | Tester |
| Merge | `pr_safe_merge.ps1` | DevOps |
| View prompts | `prompt_list.ps1` | Any |
| Full cycle | `team_cycle.ps1` | All |

---

## Support

For questions or issues:
1. Check relevant documentation in `docs/team/`
2. Review existing prompts in `prompts/`
3. Check `README.md` for setup instructions
4. Ask user for clarification
