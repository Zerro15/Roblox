# Team Status Prompt

## Task
Check the current status of the Roblox Tower Defense prototype project.

## Instructions

### 1. Git Status
```powershell
# Current branch and uncommitted changes
git status

# Recent commits
git log --oneline -10

# Current branch
git branch --show-current
```

**What to report:**
- Current branch
- Uncommitted changes (if any)
- Recent commits
- Commits since last release

### 2. PR Status
```powershell
# Open PRs
gh pr list --state open

# PR details
gh pr view <PR_NUMBER>
```

**What to report:**
- Number of open PRs
- PR titles and numbers
- PR status (draft, ready, checks passing)
- PR authors
- Days since opened

### 3. Game State
- Read `docs/team/CURRENT_STATE.md`
- List implemented features
- List pending features
- Note any known issues

**What to report:**
- Implemented features
- Partially working features
- Pending features
- Known issues

### 4. Build Status
```powershell
# Check if build exists
ls -la build/game.rbxlx

# Check build date
(Get-Item build/game.rbxlx).LastWriteTime
```

**What to report:**
- Build exists (yes/no)
- Build date
- Build size

### 5. Test Status
- Check `logs/demo_test_report.md`
- Review latest test results
- Note any failures

**What to report:**
- Last test date
- Last test status
- Any failures
- Performance notes

### 6. Process State
```powershell
# Check Studio Operator state
.\scripts\operator_status.ps1
```

**What to report:**
- Running processes
- Last operation
- Any stuck processes

## Output Format

Provide a comprehensive status report:

```
# Team Status Report

## Git Status
- **Current Branch:** [branch name]
- **Uncommitted Changes:** [count or "clean"]
- **Recent Commits:** [list last 3]
- **Days Since Last Commit:** [N]

## Pull Requests
- **Open PRs:** [count]
- **PR List:**
  - #[N] - [Title] - [Status] - [Days open]
  - #[N] - [Title] - [Status] - [Days open]

## Game State

### Implemented Features
- ✅ Enemy movement along path nodes
- ✅ Tower targeting and damage
- ✅ Reward economy
- ✅ Wave progression
- ✅ Greymoor Veil District map
- ✅ Demo recorder

### Pending Features
- ⏳ Tower placement spending
- ⏳ UI money display
- ⏳ Projectile visuals
- ⏳ Base health/lives system
- ⏳ Gacha unit system

### Known Issues
- [List any known issues]

## Build Status
- **Build Exists:** Yes/No
- **Build Date:** [Date]
- **Build Size:** [MB]
- **Build Path:** build/game.rbxlx

## Test Status
- **Last Test:** [Date]
- **Last Test Status:** ✅ PASSED / ❌ FAILED
- **Test Report:** logs/demo_test_report.md
- **Video:** logs/recordings/[latest]

## Process State
- **Bridge:** [Running/Stopped]
- **Rojo:** [Running/Stopped]
- **Studio:** [Open/Closed]
- **Issues:** [List any issues]

## Summary
- **Overall Status:** ✅ HEALTHY / ⏳ IN PROGRESS / ❌ ISSUES
- **Next Action:** [Recommended next step]
- **Blockers:** [Any blocking issues]

## Recommendations
- [Suggestion 1]
- [Suggestion 2]
```

## Status Interpretation

### Healthy Status
- ✅ Clean working tree
- ✅ All checks passing
- ✅ Recent commits
- ✅ No open issues
- ✅ Recent successful test

### In Progress
- ⏳ Open PRs waiting for review
- ⏳ Recent commits
- ⏳ Build exists but not tested
- ⏳ Some features pending

### Issues
- ❌ Uncommitted changes
- ❌ Failing checks
- ❌ Old build
- ❌ Failed tests
- ❌ Stuck processes

## Key Metrics

**Velocity:**
- Commits per week
- PRs merged per week
- Features completed per week

**Quality:**
- Test pass rate
- Build success rate
- Regression rate

**Health:**
- Days since last commit
- Days since last test
- Number of open issues
- Number of open PRs

## Questions to Answer

1. **Is the project healthy?**
   - Check: clean tree, recent commits, passing tests

2. **What's the current focus?**
   - Check: open PRs, recent commits

3. **What's next?**
   - Check: ROADMAP.md, NEXT_ACTIONS.md

4. **Are there blockers?**
   - Check: failing tests, stuck processes, conflicts

5. **When was the last release?**
   - Check: git tags, recent merges

## Success Criteria

Status report is complete when:
- ✅ Git status checked
- ✅ PR status checked
- ✅ Game state reviewed
- ✅ Build status verified
- ✅ Test status checked
- ✅ Process state verified
- ✅ Summary provided
- ✅ Recommendations given
