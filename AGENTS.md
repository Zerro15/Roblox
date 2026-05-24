# AGENTS.md: Codex CLI Agent Configuration

## Overview

This document defines agent roles, responsibilities, and communication patterns for Codex CLI integration with the Roblox Tower Defense prototype.

**Status:** Ready for Codex CLI integration (currently using Claude directly)

---

## Agent Roles

### 1. Architect Agent
**Responsibility:** Design, planning, and strategic decisions

**Capabilities:**
- Analyze codebase structure
- Design new features and systems
- Create implementation plans
- Review design decisions
- Identify technical risks

**Constraints:**
- Must not modify game code without explicit approval
- Must preserve existing Studio Operator and PR manager
- Must follow safe PR merge protocols

**Prompts:**
- `prompts/design_feature.md`
- `prompts/audit_codebase.md`

**Handoff to:** Developer Agent (with detailed design plan)

---

### 2. Developer Agent
**Responsibility:** Code implementation and integration

**Capabilities:**
- Implement features from design specs
- Write Lua game code and Python tools
- Integrate with existing systems
- Create unit tests
- Maintain code style and patterns

**Constraints:**
- Must follow Architect's design plan
- Must not commit build/ or logs/
- Must not add secrets or tokens
- Must preserve game code structure

**Prompts:**
- `prompts/implement_code.md`
- `prompts/test_game.md`

**Handoff to:** Tester Agent (with PR ready for review)

---

### 3. Tester Agent
**Responsibility:** Quality assurance and verification

**Capabilities:**
- Run demo tests via Studio Operator
- Verify game logic and features
- Collect Roblox logs and analyze
- Create test reports
- Identify regressions

**Constraints:**
- Must use safe Studio Operator flows
- Must not force-push or merge PRs
- Must document all findings

**Prompts:**
- `prompts/test_game.md`
- `prompts/review_pr.md`

**Handoff to:** DevOps Agent (with test report and approval)

---

### 4. DevOps Agent
**Responsibility:** Build, deployment, and CI/CD

**Capabilities:**
- Run safe PR merge checks
- Manage git workflow
- Execute build pipeline
- Monitor process state
- Orchestrate team cycles

**Constraints:**
- Must verify all safety checks pass
- Must not merge without Tester approval
- Must not commit build artifacts

**Prompts:**
- `prompts/team_status.md`
- `prompts/team_plan.md`

**Handoff to:** Architect Agent (cycle complete, ready for next feature)

---

## Communication Patterns

### Standard Workflow

```
Architect → Design Plan
    ↓
Developer → Implementation + PR
    ↓
Tester → Test Report + Approval
    ↓
DevOps → Safe Merge + Cycle Complete
    ↓
Architect → Next Feature
```

### Handoff Protocol

Each handoff includes:

1. **Explicit status** - what is complete, what is pending
2. **Artifacts** - files, PRs, reports, logs
3. **Constraints** - what the next agent must respect
4. **Success criteria** - how to verify the handoff is complete

### Communication Medium

- **Status updates:** `team_orchestrator.py status`
- **Planning:** `team_orchestrator.py plan_next`
- **Demo review:** `team_orchestrator.py review_demo`
- **Cycle execution:** `team_orchestrator.py cycle`

---

## Safety Rules (All Agents)

### Git & PR Management
- ✅ Clean working tree before operations
- ✅ Verify `gh auth status` before PR operations
- ✅ Use `pr_safe_merge.ps1` for merging
- ❌ No force push
- ❌ No merge without checks passing

### Build & Studio
- ✅ Use `rojo build` via `build_place.ps1`
- ✅ Use Studio Operator safe flows
- ✅ Verify build artifacts exist
- ❌ No manual Studio modifications without bridge
- ❌ No commit of `build/game.rbxlx`

### Game Code
- ✅ Modify only `src/` for game features
- ✅ Follow existing Lua patterns
- ✅ Add configs to `src/shared/configs/`
- ✅ Add services to `src/server/services/`
- ❌ No modification of bridge or bootstrap code without Architect approval

### Secrets & Artifacts
- ❌ No API keys, tokens, or `.env` in commits
- ❌ No `logs/`, `screenshots/`, `recordings/` in commits
- ❌ No `venv/` or `.venv*` in commits
- ✅ Use `.gitignore` for sensitive files

---

## Feature Development Cycle

### Phase 1: Planning (Architect)
1. Review current state (`docs/team/CURRENT_STATE.md`)
2. Check roadmap (`docs/team/ROADMAP.md`)
3. Design feature with constraints
4. Create implementation plan
5. Handoff to Developer

### Phase 2: Implementation (Developer)
1. Read design plan
2. Implement feature in `src/`
3. Add configs if needed
4. Create PR with description
5. Handoff to Tester

### Phase 3: Testing (Tester)
1. Run demo via `team_review_demo.ps1`
2. Collect logs and screenshots
3. Verify game logic
4. Create test report
5. Approve or request changes
6. Handoff to DevOps

### Phase 4: Merge (DevOps)
1. Verify all checks pass
2. Run `pr_safe_merge.ps1`
3. Update `docs/team/CURRENT_STATE.md`
4. Handoff to Architect (cycle complete)

---

## Model Routing Policy

All agents must follow the model routing policy to select appropriate AI models:

### Model Levels
- **Quick (haiku):** Documentation, status, simple scripts
- **Code (sonnet):** Feature implementation, bug fixes
- **Deep (opus/opusplan):** Architecture, security, risky operations
- **Verify (haiku/sonnet):** Testing, log analysis, verification

### Rules for Codex Agents
1. **Determine task mode** before starting
2. **Select appropriate profile** (quick/code/deep/verify)
3. **Codex will recommend** if current model is insufficient
4. **Explicit notification** if switching models mid-task
5. **No silent model changes** during task execution

### Recommendation Format
When model is insufficient:
```
Task: "Fix PR safe merge manager bug"
Current profile: code
Recommended profile: deep
Reason: PR manager changes require deep reasoning for safety
Recommendation: Switch to deep profile? (y/n)
```

### Safety Rules for Model Selection
- ❌ Never use Quick for risky merge/security/hard architecture
- ❌ Never use Code for PR manager changes
- ✅ Always use Deep for architecture and security
- ✅ Always use Deep for merge safety verification
- ✅ Use Code for normal feature work
- ✅ Use Quick for documentation and status

See `docs/team/MODEL_ROUTING.md` for detailed policy.

## Integration with Claude

When Codex CLI is unavailable, Claude acts as all agents:

1. **Plan mode:** Claude designs feature (Architect role)
2. **Implementation mode:** Claude implements code (Developer role)
3. **Verification mode:** Claude runs tests (Tester role)
4. **Merge mode:** Claude executes safe merge (DevOps role)

Claude follows the same safety rules, handoff protocols, and **model routing policy**.

---

## Tools & Scripts

### Team Orchestrator
```powershell
python .\tools\studio_operator\team_orchestrator.py --action status
python .\tools\studio_operator\team_orchestrator.py --action plan_next
python .\tools\studio_operator\team_orchestrator.py --action review_demo
python .\tools\studio_operator\team_orchestrator.py --action cycle
```

### Wrapper Scripts
```powershell
.\scripts\team_status.ps1
.\scripts\team_plan_next.ps1
.\scripts\team_review_demo.ps1
.\scripts\team_cycle.ps1
```

### Prompt Management
```powershell
.\scripts\prompt_list.ps1
.\scripts\prompt_show.ps1 -Name design_feature
```

---

## Current Status

- ✅ Rojo build pipeline working
- ✅ Studio Operator v4 operational
- ✅ Safe PR manager in place
- ✅ Game foundation complete
- ⏳ Codex CLI integration pending
- ⏳ Team orchestrator pending

See `docs/team/CURRENT_STATE.md` for detailed game state.

---

## Next Steps

1. Implement team_orchestrator.py
2. Create prompt templates in prompts/
3. Create team documentation in docs/team/
4. Test all scripts and workflows
5. Integrate with Codex CLI when available
