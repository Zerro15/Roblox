# ROLES.md: Team Member Roles and Responsibilities

## Overview

This document defines roles for the Roblox Tower Defense prototype development team.

---

## Role: Architect

**Responsibility:** Design, planning, and strategic decisions

### Capabilities
- Analyze codebase structure and patterns
- Design new features and systems
- Create detailed implementation plans
- Review design decisions and trade-offs
- Identify technical risks and mitigation strategies
- Plan roadmap and prioritize features
- Mentor other team members on architecture

### Typical Tasks
- Review feature requests and create design documents
- Analyze codebase for patterns and best practices
- Design new services and systems
- Plan feature dependencies and timeline
- Review PRs for architectural correctness
- Identify technical debt and refactoring needs
- Plan major system changes

### Success Metrics
- ✅ Designs are clear and implementable
- ✅ Plans are accurate and realistic
- ✅ Risks are identified and mitigated
- ✅ Team understands architecture
- ✅ Code follows designed patterns

### Tools & Scripts
- `prompts/audit_codebase.md` - Analyze code
- `prompts/design_feature.md` - Design features
- `docs/team/ROADMAP.md` - Plan timeline
- `docs/team/DEVELOPMENT_LOOP.md` - Define process

---

## Role: Developer

**Responsibility:** Code implementation and integration

### Capabilities
- Implement features from design specifications
- Write Lua game code following project patterns
- Write Python tools and utilities
- Integrate with existing systems
- Create unit tests and test code
- Maintain code style and conventions
- Debug and fix issues

### Typical Tasks
- Implement features from approved designs
- Write new services and configs
- Integrate with existing services
- Create PR with clear descriptions
- Respond to code review feedback
- Fix bugs and regressions
- Write tests for new code

### Success Metrics
- ✅ Code follows project patterns
- ✅ Features work as designed
- ✅ Code is well-commented
- ✅ Tests pass
- ✅ No regressions introduced
- ✅ PRs are clear and focused

### Tools & Scripts
- `prompts/implement_code.md` - Implementation guide
- `prompts/test_game.md` - Testing guide
- `scripts/build_place.ps1` - Build game
- `scripts/auto_play_assisted.ps1` - Test game

---

## Role: Tester

**Responsibility:** Quality assurance and verification

### Capabilities
- Run demo tests via Studio Operator
- Verify game logic and features
- Collect and analyze Roblox logs
- Create detailed test reports
- Identify regressions and edge cases
- Verify performance and stability
- Document test results

### Typical Tasks
- Run demo tests for new features
- Verify features work as designed
- Check for regressions in existing features
- Analyze Roblox logs for errors
- Create test reports
- Approve or request changes to PRs
- Test edge cases and error conditions

### Success Metrics
- ✅ All features tested thoroughly
- ✅ Regressions caught early
- ✅ Test reports are detailed
- ✅ Issues documented clearly
- ✅ No bugs slip to production
- ✅ Performance acceptable

### Tools & Scripts
- `prompts/test_game.md` - Testing guide
- `prompts/review_pr.md` - PR review guide
- `scripts/team_review_demo.ps1` - Run demo test
- `logs/demo_test_report.md` - Test results

---

## Role: DevOps

**Responsibility:** Build, deployment, and CI/CD

### Capabilities
- Run safe PR merge checks
- Manage git workflow and branches
- Execute build pipeline
- Monitor process state and health
- Orchestrate team cycles
- Manage GitHub integration
- Handle deployment and releases

### Typical Tasks
- Verify PR checks pass
- Run safe merge process
- Manage git branches and commits
- Execute build pipeline
- Monitor process state
- Orchestrate team cycles
- Update documentation after merges
- Handle releases and tags

### Success Metrics
- ✅ All merges are safe
- ✅ Build pipeline works reliably
- ✅ No broken builds
- ✅ Process state is clean
- ✅ Deployments are smooth
- ✅ No data loss or corruption

### Tools & Scripts
- `scripts/pr_safe_merge.ps1` - Safe merge
- `scripts/build_place.ps1` - Build game
- `scripts/team_status.ps1` - Check status
- `tools/studio_operator/team_orchestrator.py` - Orchestration

---

## Team Structure

### Single Developer Team
When one person handles all roles:

1. **Plan Mode** - Architect role
   - Design features
   - Plan implementation
   - Create design documents

2. **Implementation Mode** - Developer role
   - Write code
   - Create PRs
   - Respond to feedback

3. **Testing Mode** - Tester role
   - Run demos
   - Verify features
   - Create test reports

4. **Merge Mode** - DevOps role
   - Run safe merge
   - Update documentation
   - Commit changes

### Multi-Person Team
When roles are distributed:

- **Architect** - Designs features, plans roadmap
- **Developer** - Implements features, writes code
- **Tester** - Tests features, verifies quality
- **DevOps** - Manages builds, merges, releases

---

## Role Transitions

### Architect → Developer
**Handoff includes:**
- Approved design document
- List of affected files
- Implementation steps
- Success criteria
- Risk assessment

### Developer → Tester
**Handoff includes:**
- Completed PR
- Feature description
- Test scenarios
- Expected behavior
- Known limitations

### Tester → DevOps
**Handoff includes:**
- Test report
- Approval or rejection
- Issues found (if any)
- Recommendations
- Ready for merge status

### DevOps → Architect
**Handoff includes:**
- Merge confirmation
- Updated documentation
- New game state
- Next feature ready to plan

---

## Skill Requirements

### Architect
- **Required:** Lua, system design, architecture patterns
- **Helpful:** Python, git, Roblox API knowledge
- **Soft Skills:** Communication, planning, mentoring

### Developer
- **Required:** Lua, git, Roblox API
- **Helpful:** Python, testing, debugging
- **Soft Skills:** Attention to detail, problem-solving

### Tester
- **Required:** Game testing, log analysis, attention to detail
- **Helpful:** Lua, Python, performance profiling
- **Soft Skills:** Communication, documentation, thoroughness

### DevOps
- **Required:** Git, PowerShell, build systems
- **Helpful:** Python, GitHub CLI, process management
- **Soft Skills:** Reliability, attention to detail, automation

---

## Responsibilities Matrix

| Task | Architect | Developer | Tester | DevOps |
|------|-----------|-----------|--------|--------|
| Design features | ✅ | - | - | - |
| Implement code | - | ✅ | - | - |
| Code review | ✅ | ✅ | - | - |
| Test features | - | ✅ | ✅ | - |
| Verify quality | ✅ | - | ✅ | - |
| Merge PRs | - | - | - | ✅ |
| Build game | - | ✅ | ✅ | ✅ |
| Update docs | ✅ | ✅ | ✅ | ✅ |
| Plan roadmap | ✅ | - | - | - |
| Monitor health | ✅ | - | - | ✅ |

---

## Communication Protocol

### Daily Standup
- **What did you do?** - Yesterday's work
- **What will you do?** - Today's plan
- **Blockers?** - Any issues or dependencies

### Design Review
- Architect presents design
- Team discusses and questions
- Approval before implementation

### Code Review
- Architect reviews for design compliance
- Developer reviews for code quality
- Tester reviews for test coverage

### Test Review
- Tester presents test results
- Team discusses findings
- Approval before merge

### Merge Review
- DevOps verifies all checks pass
- Team confirms no regressions
- Safe merge executed

---

## Escalation Path

**Issue Resolution:**
1. Try to resolve within role
2. Discuss with related role
3. Escalate to Architect
4. Team decision if needed

**Example:**
- Developer finds design issue → Discuss with Architect
- Tester finds regression → Discuss with Developer
- DevOps finds merge issue → Discuss with team

---

## Training & Development

### For New Architects
- Study `AGENTS.md` and `CLAUDE.md`
- Review `docs/team/ROADMAP.md`
- Analyze existing services in `src/server/services/`
- Study `prompts/design_feature.md`

### For New Developers
- Study `CLAUDE.md` and `prompts/implement_code.md`
- Review existing code patterns in `src/`
- Study `src/server/services/` examples
- Practice with small features

### For New Testers
- Study `prompts/test_game.md`
- Learn Studio Operator usage
- Practice running demos
- Study log analysis

### For New DevOps
- Study git workflow
- Learn Studio Operator
- Practice safe merge process
- Study `tools/studio_operator/README.md`

---

## Performance Evaluation

### Architect
- Design quality and clarity
- Risk identification accuracy
- Roadmap accuracy
- Team feedback and mentoring

### Developer
- Code quality and patterns
- Feature completeness
- Bug rate and regressions
- Code review feedback

### Tester
- Test coverage and thoroughness
- Bug detection rate
- Report quality and clarity
- Regression prevention

### DevOps
- Merge safety and reliability
- Build success rate
- Process automation
- Team support and documentation

---

## Notes

- Roles can overlap - one person can have multiple roles
- Roles are flexible - can be adjusted based on team needs
- Communication is key - clear handoffs prevent issues
- Documentation is essential - helps team understand decisions
