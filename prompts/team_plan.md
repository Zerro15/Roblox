# Team Plan Prompt

## Task
Plan the next tasks for the Roblox Tower Defense prototype development.

## Instructions

### 1. Review Current State
- Read `docs/team/CURRENT_STATE.md` - what's done?
- Read `docs/team/ROADMAP.md` - what's planned?
- Read `docs/team/NEXT_ACTIONS.md` - what's next?
- Check git log - what was recently done?

### 2. Assess Blockers
- Are there any blocking issues?
- Are there any stuck PRs?
- Are there any failing tests?
- Are there any technical debt items?

### 3. Review Roadmap
- What's the priority?
- What's the timeline?
- What are the dependencies?
- What's the effort estimate?

### 4. Identify Next Tasks
Based on:
- Current state
- Roadmap priorities
- Dependencies
- Team capacity
- Risk assessment

### 5. Prioritize Tasks
- What should be done first?
- What depends on what?
- What has highest impact?
- What is highest risk?

### 6. Create Action Plan
- Define 3-5 next tasks
- Estimate effort for each
- Identify dependencies
- Note any risks

### 7. Provide Recommendations
- What should the team focus on?
- What should be avoided?
- What needs attention?
- What's the next milestone?

## Output Format

Provide a detailed plan:

```
# Team Plan: Next Tasks

## Current Status Summary
- **Last Commit:** [Date] - [Message]
- **Open PRs:** [Count]
- **Last Test:** [Date] - [Status]
- **Build Status:** [Status]

## Blockers & Issues
- [Issue 1]
- [Issue 2]

## Roadmap Context
- **Phase:** [Current phase]
- **Timeline:** [Estimated completion]
- **Priority:** [High/Medium/Low]

## Next Tasks (Prioritized)

### Task 1: [Name]
- **Description:** [What needs to be done?]
- **Type:** Feature / Bug Fix / Refactor / Documentation
- **Effort:** [Hours estimate]
- **Priority:** [High/Medium/Low]
- **Dependencies:** [What must be done first?]
- **Success Criteria:** [How to verify it's done?]
- **Risks:** [What could go wrong?]

### Task 2: [Name]
- **Description:** [What needs to be done?]
- **Type:** Feature / Bug Fix / Refactor / Documentation
- **Effort:** [Hours estimate]
- **Priority:** [High/Medium/Low]
- **Dependencies:** [What must be done first?]
- **Success Criteria:** [How to verify it's done?]
- **Risks:** [What could go wrong?]

### Task 3: [Name]
- **Description:** [What needs to be done?]
- **Type:** Feature / Bug Fix / Refactor / Documentation
- **Effort:** [Hours estimate]
- **Priority:** [High/Medium/Low]
- **Dependencies:** [What must be done first?]
- **Success Criteria:** [How to verify it's done?]
- **Risks:** [What could go wrong?]

## Implementation Strategy

### Immediate (This Week)
- Task 1: [Name]
- Task 2: [Name]

### Short Term (Next 2 Weeks)
- Task 3: [Name]
- Task 4: [Name]

### Medium Term (Next Month)
- Task 5: [Name]
- Task 6: [Name]

## Resource Allocation
- **Developer:** [Task assignment]
- **Tester:** [Task assignment]
- **DevOps:** [Task assignment]

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| [Risk] | [Impact] | [Prob] | [How to prevent] |

## Recommendations

### Focus Areas
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

### Avoid
- [What to avoid]
- [What to defer]

### Technical Debt
- [Items to address]

### Next Milestone
- **Goal:** [What should be achieved?]
- **Timeline:** [When?]
- **Success Criteria:** [How to verify?]

## Questions for Team
- [Question 1]
- [Question 2]
```

## Task Categories

### Features
- New game mechanics
- UI improvements
- Performance optimizations
- Content additions

### Bug Fixes
- Crashes or errors
- Incorrect behavior
- Regressions
- Edge cases

### Refactoring
- Code cleanup
- Architecture improvements
- Test coverage
- Documentation

### Documentation
- README updates
- Code comments
- Team guides
- API documentation

## Effort Estimation

**Small (1-2 hours):**
- Simple bug fixes
- Small config changes
- Documentation updates
- Minor UI tweaks

**Medium (4-8 hours):**
- New feature with existing patterns
- Moderate refactoring
- Integration with existing systems
- Test coverage additions

**Large (16+ hours):**
- New system/service
- Major refactoring
- Complex feature
- Architecture changes

## Priority Criteria

**High Priority:**
- Blocks other work
- Critical bug
- Core feature
- High impact

**Medium Priority:**
- Improves experience
- Reduces technical debt
- Enables future work
- Moderate impact

**Low Priority:**
- Nice to have
- Can be deferred
- Low impact
- Low urgency

## Dependency Analysis

**Identify:**
- What must be done first?
- What can be done in parallel?
- What blocks future work?
- What are the critical path items?

**Example:**
```
Tower Placement Spending
  ├─ Requires: EconomyService (✅ done)
  ├─ Requires: TowerService (✅ done)
  └─ Enables: UI Money Display (⏳ pending)
```

## Success Criteria Template

For each task:
- ✅ Code implemented
- ✅ Tests pass
- ✅ No regressions
- ✅ Documentation updated
- ✅ PR merged
- ✅ Feature verified in game

## Risk Mitigation

**Common Risks:**
- **Scope creep:** Stick to design, avoid adding features
- **Regressions:** Test thoroughly, verify existing features
- **Dependencies:** Identify and communicate blockers
- **Performance:** Profile and optimize before release
- **Technical debt:** Schedule refactoring tasks

## Success Criteria

Plan is complete when:
- ✅ Current state understood
- ✅ Blockers identified
- ✅ Next 3-5 tasks defined
- ✅ Priorities clear
- ✅ Effort estimated
- ✅ Dependencies identified
- ✅ Risks assessed
- ✅ Recommendations provided
