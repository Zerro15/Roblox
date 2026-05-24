# DEVELOPMENT_LOOP.md: Standard Development Cycle

## Overview

This document defines the standard development cycle for the Roblox Tower Defense prototype.

**Cycle Duration:** 1-2 weeks per feature
**Phases:** Plan → Implement → Test → Merge

---

## Phase 1: Planning (Architect Role)

### Duration
- **Small feature:** 1-2 hours
- **Medium feature:** 2-4 hours
- **Large feature:** 4-8 hours

### Activities

1. **Review Current State**
   - Read `CURRENT_STATE.md`
   - Check `ROADMAP.md`
   - Identify next feature

2. **Analyze Requirements**
   - What problem does this solve?
   - What is the user-facing behavior?
   - How does it fit into the game loop?

3. **Explore Existing Code**
   - Read related services
   - Review related configs
   - Identify patterns and conventions

4. **Design Solution**
   - Architecture and components
   - Affected files and changes
   - Implementation steps
   - Success criteria

5. **Create Design Document**
   - Use `prompts/design_feature.md`
   - Document architecture
   - List affected files
   - Define success criteria

6. **Get Approval**
   - Present design to team
   - Answer questions
   - Incorporate feedback
   - Get final approval

### Deliverables
- ✅ Design document
- ✅ List of affected files
- ✅ Implementation steps
- ✅ Success criteria
- ✅ Risk assessment

### Success Criteria
- Design is clear and implementable
- All affected files identified
- Steps are logical and ordered
- Success criteria are measurable
- Team understands and approves

---

## Phase 2: Implementation (Developer Role)

### Duration
- **Small feature:** 2-4 hours
- **Medium feature:** 4-8 hours
- **Large feature:** 8-16 hours

### Activities

1. **Prepare Environment**
   - Verify clean working tree: `git status`
   - Create feature branch: `git checkout -b feature/name`
   - Verify build works: `.\scripts\build_place.ps1`

2. **Implement Step by Step**
   - Read design document
   - For each implementation step:
     - Read affected file
     - Identify change location
     - Make minimal edit
     - Verify syntax
     - Test build

3. **Follow Code Patterns**
   - Use existing service patterns
   - Use existing config patterns
   - Follow naming conventions
   - Add clear comments

4. **Add Tests**
   - Create test scenarios
   - Document expected behavior
   - Prepare test cases

5. **Verify Build**
   - Run `.\scripts\build_place.ps1`
   - Check for Lua errors
   - Verify all imports correct
   - Check file syntax

6. **Create PR**
   - Stage changes: `git add src/`
   - Commit: `git commit -m "Add feature description"`
   - Push: `git push origin feature/name`
   - Create PR: `gh pr create --title "..." --body "..."`

### Deliverables
- ✅ Code implementation
- ✅ Feature branch
- ✅ PR with description
- ✅ Build verification
- ✅ Test scenarios

### Success Criteria
- All design requirements met
- Code follows project patterns
- Build succeeds
- No syntax errors
- PR is clear and focused

---

## Phase 3: Testing (Tester Role)

### Duration
- **Small feature:** 1-2 hours
- **Medium feature:** 2-4 hours
- **Large feature:** 4-8 hours

### Activities

1. **Prepare Test Environment**
   - Checkout PR branch
   - Build game: `.\scripts\build_place.ps1`
   - Verify build succeeded

2. **Run Demo Test**
   - Execute: `.\scripts\team_review_demo.ps1`
   - Or assisted mode: `.\scripts\auto_play_assisted.ps1`
   - Record video and screenshots
   - Collect logs

3. **Test Feature Behavior**
   - Verify feature initializes
   - Test main functionality
   - Test edge cases
   - Check error handling

4. **Verify No Regressions**
   - Test existing features
   - Check for new errors
   - Verify performance
   - Check logs for warnings

5. **Analyze Results**
   - Review video recording
   - Review screenshots
   - Analyze Roblox logs
   - Check demo report

6. **Create Test Report**
   - Use `prompts/test_game.md`
   - Document test scenarios
   - List results
   - Provide approval or feedback

### Deliverables
- ✅ Test report
- ✅ Video recording
- ✅ Screenshots
- ✅ Log analysis
- ✅ Approval or feedback

### Success Criteria
- All test scenarios pass
- No regressions found
- Logs are clean
- Feature works as designed
- Ready for merge

---

## Phase 4: Merge (DevOps Role)

### Duration
- **All features:** 15-30 minutes

### Activities

1. **Verify Preconditions**
   - Working tree is clean: `git status`
   - gh auth is active: `gh auth status`
   - PR checks pass: `gh pr checks <N>`

2. **Run Safe Merge**
   - Execute: `.\scripts\pr_safe_merge.ps1 -PrNumber <N>`
   - Verify merge succeeds
   - Verify no conflicts

3. **Update Documentation**
   - Update `CURRENT_STATE.md`
   - Add feature to implemented list
   - Update game state

4. **Commit Changes**
   - Stage: `git add docs/`
   - Commit: `git commit -m "Update state after merge"`
   - Push: `git push origin main`

5. **Verify Merge**
   - Check main branch: `git log --oneline -5`
   - Verify PR is closed
   - Verify build still works

### Deliverables
- ✅ Merged PR
- ✅ Updated documentation
- ✅ Clean main branch
- ✅ Merge confirmation

### Success Criteria
- PR merged successfully
- No conflicts
- All checks passed
- Documentation updated
- Main branch clean

---

## Cycle Workflow

## Cycle Workflow

### Day 1: Planning
```
Morning:
  - Architect reviews roadmap
  - Architect selects model (Quick or Code for design)
  - Architect designs feature
  - Team discusses design
  
Afternoon:
  - Design approved
  - Developer ready to implement
```

### Day 2-3: Implementation
```
Morning:
  - Developer selects model (Code for implementation)
  - Developer implements feature
  - Developer verifies build
  
Afternoon:
  - Developer creates PR
  - Tester begins testing
```

### Day 4: Testing & Merge
```
Morning:
  - Tester selects model (Verify for testing)
  - Tester runs demo test
  - Tester analyzes results
  
Afternoon:
  - Tester approves or requests changes
  - If approved: DevOps selects model (Code or Deep for merge)
  - DevOps merges PR
  - If changes needed: Developer fixes
```

### Day 5: Verification
```
Morning:
  - Team verifies merge
  - Documentation updated
  - Cycle complete
```

---

## Parallel Workflows

### Multiple Features
When multiple features are in progress:

```
Feature 1: Plan → Implement → Test → Merge
Feature 2:          Plan → Implement → Test → Merge
Feature 3:                  Plan → Implement → Test → Merge
```

### Recommended Approach
- Max 2-3 features in parallel
- Stagger phases to avoid bottlenecks
- Prioritize by dependencies

---

## Handling Issues

### During Implementation
- **Build fails:** Fix immediately, verify syntax
- **Design issue:** Discuss with Architect, adjust if needed
- **Dependency missing:** Wait for dependency or adjust design

### During Testing
- **Feature doesn't work:** Developer fixes, re-test
- **Regression found:** Identify cause, fix, re-test
- **Performance issue:** Optimize or defer feature

### During Merge
- **Checks fail:** Investigate, fix, re-run checks
- **Conflicts:** Resolve conflicts, re-test
- **Documentation issue:** Update docs, re-commit

---

## Cycle Variations

### Quick Cycle (Small Feature)
- Planning: 1 hour
- Implementation: 2 hours
- Testing: 1 hour
- Merge: 15 minutes
- **Total:** ~4.5 hours

### Standard Cycle (Medium Feature)
- Planning: 2 hours
- Implementation: 6 hours
- Testing: 2 hours
- Merge: 15 minutes
- **Total:** ~10 hours

### Extended Cycle (Large Feature)
- Planning: 4 hours
- Implementation: 12 hours
- Testing: 4 hours
- Merge: 15 minutes
- **Total:** ~20 hours

---

## Communication

### Daily Standup
**When:** Start of day
**Duration:** 15 minutes
**Attendees:** All roles

**Agenda:**
- What did you do yesterday?
- What will you do today?
- Any blockers?

### Design Review
**When:** After planning phase
**Duration:** 30 minutes
**Attendees:** Architect, Developer, Tester

**Agenda:**
- Present design
- Discuss approach
- Identify risks
- Get approval

### Code Review
**When:** After PR created
**Duration:** 30 minutes
**Attendees:** Developer, Architect, Tester

**Agenda:**
- Review code quality
- Check design compliance
- Identify issues
- Approve or request changes

### Test Review
**When:** After testing complete
**Duration:** 30 minutes
**Attendees:** Tester, Developer, DevOps

**Agenda:**
- Present test results
- Discuss findings
- Approve or request changes
- Plan merge

---

## Tools & Scripts

### Planning
- `prompts/design_feature.md` - Design template
- `docs/team/ROADMAP.md` - Feature roadmap
- `docs/team/CURRENT_STATE.md` - Current state

### Implementation
- `prompts/implement_code.md` - Implementation guide
- `scripts/build_place.ps1` - Build game
- Text editor for code

### Testing
- `prompts/test_game.md` - Testing guide
- `scripts/team_review_demo.ps1` - Run demo
- `scripts/auto_play_assisted.ps1` - Assisted mode

### Merge
- `scripts/pr_safe_merge.ps1` - Safe merge
- `scripts/pr_status.ps1` - Check PR status
- Git CLI

---

## Metrics & Tracking

### Cycle Metrics
- **Cycle time:** Days from plan to merge
- **Implementation time:** Hours to implement
- **Test time:** Hours to test
- **Merge time:** Minutes to merge

### Quality Metrics
- **Build success rate:** % of builds that succeed
- **Test pass rate:** % of tests that pass
- **Regression rate:** % of features with regressions
- **Bug rate:** Bugs per feature

### Team Metrics
- **Features per week:** Features completed
- **Velocity:** Hours per feature
- **Efficiency:** Actual vs estimated time

---

## Continuous Improvement

### Weekly Review
- What went well?
- What could be improved?
- What should we change?

### Monthly Retrospective
- Review cycle metrics
- Identify bottlenecks
- Plan improvements
- Adjust process

---

## Notes

- Cycle duration varies by feature complexity
- Parallel workflows increase throughput
- Communication is key to smooth cycles
- Regular reviews help improve process
- Flexibility is important

---

## Questions?

Refer to:
- `ROLES.md` - Team roles
- `CURRENT_STATE.md` - Current game state
- `ROADMAP.md` - Feature roadmap
- `prompts/` - Detailed guidance
