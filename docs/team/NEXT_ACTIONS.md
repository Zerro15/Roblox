# NEXT_ACTIONS.md: Next 3-5 Actionable Tasks

## Current Status
**Date:** 2026-05-24
**Phase:** Core Features (Phase 2)
**Progress:** Foundation complete, ready for feature development

---

## Next 5 Tasks (Prioritized)

### Task 1: Tower Placement Spending System ⏳ HIGH PRIORITY
**Type:** Feature
**Effort:** 4-8 hours
**Priority:** High
**Status:** Ready to start
**Recommended Mode:** Code (sonnet)

**Description:**
Implement tower placement spending - deduct money from player when placing towers.

**What needs to be done:**
1. Add tower costs to `TowerConfig.lua`
2. Modify `TowerService.lua` to check money before placement
3. Integrate with `EconomyService.lua` to deduct money
4. Add validation to prevent placement if insufficient funds
5. Add logs for placement attempts and costs

**Success Criteria:**
- ✅ Tower costs defined in config
- ✅ Money deducted on successful placement
- ✅ Cannot place tower if insufficient funds
- ✅ Logs show placement cost and result
- ✅ Demo test passes

**Affected Files:**
- `src/shared/configs/TowerConfig.lua` - Add costs
- `src/server/services/TowerService.lua` - Add spending logic
- `src/server/services/EconomyService.lua` - Add deduction method

**Dependencies:**
- EconomyService ✅ (already implemented)
- TowerService ✅ (already implemented)

**Risks:**
- None identified

**Next Steps:**
1. Design feature (1-2 hours)
2. Implement changes (2-4 hours)
3. Test via demo (1-2 hours)
4. Merge via safe merge (15 min)

---

### Task 2: UI Money Display System ⏳ HIGH PRIORITY
**Type:** Feature
**Effort:** 4-8 hours
**Priority:** High
**Status:** Ready after Task 1
**Recommended Mode:** Code (sonnet)

**Description:**
Display player money in GUI so players can see their current balance.

**What needs to be done:**
1. Create GUI in `StarterGui`
2. Add TextLabel for money display
3. Connect to `EconomyService` for updates
4. Update display when money changes
5. Style consistently with game theme

**Success Criteria:**
- ✅ Money display visible in corner
- ✅ Updates when money changes
- ✅ Shows current money amount
- ✅ Styled consistently
- ✅ Demo test passes

**Affected Files:**
- `src/client/Main.client.lua` - Add GUI code
- `src/shared/GameConfig.lua` - Add GUI config if needed

**Dependencies:**
- EconomyService ✅ (already implemented)
- Task 1 (optional, but recommended)

**Risks:**
- GUI positioning may vary on different screen sizes

**Next Steps:**
1. Design feature (1-2 hours)
2. Implement GUI (2-4 hours)
3. Test via demo (1-2 hours)
4. Merge via safe merge (15 min)

---

### Task 3: Base Health/Lives System ⏳ HIGH PRIORITY
**Type:** Feature
**Effort:** 4-8 hours
**Priority:** High
**Status:** Ready after Task 2
**Recommended Mode:** Code (sonnet)

**Description:**
Add health/lives system to base - player loses lives when enemies reach exit.

**What needs to be done:**
1. Add health property to `EconomyService` or new `HealthService`
2. Modify `EnemyService` to damage base on exit
3. Add game over condition when health <= 0
4. Add health display to UI
5. Add logs for health changes

**Success Criteria:**
- ✅ Base starts with health
- ✅ Enemies deal damage on exit
- ✅ Game over when health reaches 0
- ✅ Health display in UI
- ✅ Demo test passes

**Affected Files:**
- `src/server/services/EconomyService.lua` - Add health property
- `src/server/services/EnemyService.lua` - Add damage on exit
- `src/server/Main.server.lua` - Add game over check
- `src/client/Main.client.lua` - Add health display

**Dependencies:**
- EconomyService ✅ (already implemented)
- EnemyService ✅ (already implemented)
- Task 2 (recommended for UI)

**Risks:**
- Game over logic needs careful testing

**Next Steps:**
1. Design feature (1-2 hours)
2. Implement changes (2-4 hours)
3. Test via demo (1-2 hours)
4. Merge via safe merge (15 min)

---

### Task 4: Projectile Visuals Improvement ⏳ MEDIUM PRIORITY
**Type:** Feature
**Effort:** 4-8 hours
**Priority:** Medium
**Status:** Ready after Task 3
**Recommended Mode:** Code (sonnet)

**Description:**
Improve visual effects for tower attacks - add visible projectiles instead of just beams.

**What needs to be done:**
1. Create projectile models (simple parts)
2. Modify `TowerService` to create projectiles
3. Add projectile movement to target
4. Add hit effects
5. Ensure performance acceptable

**Success Criteria:**
- ✅ Projectiles visible in flight
- ✅ Hit effects visible
- ✅ Consistent with tower type
- ✅ Performance acceptable
- ✅ Demo test passes

**Affected Files:**
- `src/server/services/TowerService.lua` - Add projectile creation
- `src/shared/configs/TowerConfig.lua` - Add projectile properties

**Dependencies:**
- TowerService ✅ (already implemented)

**Risks:**
- Performance impact if too many projectiles

**Next Steps:**
1. Design feature (1-2 hours)
2. Implement projectiles (2-4 hours)
3. Test via demo (1-2 hours)
4. Merge via safe merge (15 min)

---

### Task 5: Unit Tests for Services ⏳ MEDIUM PRIORITY
**Type:** Refactoring
**Effort:** 8-12 hours
**Priority:** Medium
**Status:** Ready after Task 4
**Recommended Mode:** Code (sonnet)

**Description:**
Add unit tests for game services to improve code quality and catch regressions.

**What needs to be done:**
1. Set up Lua testing framework
2. Create test files for each service
3. Write tests for service functions
4. Integrate tests into build pipeline
5. Document testing approach

**Success Criteria:**
- ✅ Testing framework set up
- ✅ Tests for all services
- ✅ Tests pass
- ✅ Integrated into pipeline
- ✅ Documentation complete

**Affected Files:**
- `tests/` directory (new)
- Build pipeline configuration
- Documentation

**Dependencies:**
- All services ✅ (already implemented)

**Risks:**
- Testing framework selection
- Test maintenance overhead

**Next Steps:**
1. Research Lua testing frameworks (1-2 hours)
2. Set up framework (1-2 hours)
3. Write tests (4-6 hours)
4. Integrate and document (1-2 hours)

---

## Implementation Timeline

### Week 1
- **Monday-Tuesday:** Task 1 (Tower Placement Spending)
  - Design: 1-2 hours
  - Implement: 2-4 hours
  - Test: 1-2 hours
  - Merge: 15 min

### Week 2
- **Monday-Tuesday:** Task 2 (UI Money Display)
  - Design: 1-2 hours
  - Implement: 2-4 hours
  - Test: 1-2 hours
  - Merge: 15 min

- **Wednesday-Thursday:** Task 3 (Base Health System)
  - Design: 1-2 hours
  - Implement: 2-4 hours
  - Test: 1-2 hours
  - Merge: 15 min

### Week 3
- **Monday-Tuesday:** Task 4 (Projectile Visuals)
  - Design: 1-2 hours
  - Implement: 2-4 hours
  - Test: 1-2 hours
  - Merge: 15 min

- **Wednesday-Friday:** Task 5 (Unit Tests)
  - Research: 1-2 hours
  - Setup: 1-2 hours
  - Write: 4-6 hours
  - Integrate: 1-2 hours

---

## Resource Allocation

### Architect
- Task 1: Design (1-2 hours)
- Task 2: Design (1-2 hours)
- Task 3: Design (1-2 hours)
- Task 4: Design (1-2 hours)
- Task 5: Design (1-2 hours)
- **Total:** ~5-10 hours

### Developer
- Task 1: Implement (2-4 hours)
- Task 2: Implement (2-4 hours)
- Task 3: Implement (2-4 hours)
- Task 4: Implement (2-4 hours)
- Task 5: Implement (4-6 hours)
- **Total:** ~12-22 hours

### Tester
- Task 1: Test (1-2 hours)
- Task 2: Test (1-2 hours)
- Task 3: Test (1-2 hours)
- Task 4: Test (1-2 hours)
- Task 5: Test (1-2 hours)
- **Total:** ~5-10 hours

### DevOps
- Task 1: Merge (15 min)
- Task 2: Merge (15 min)
- Task 3: Merge (15 min)
- Task 4: Merge (15 min)
- Task 5: Merge (15 min)
- **Total:** ~1.25 hours

---

## Success Metrics

### After Task 1
- ✅ Tower placement spending working
- ✅ Money deducted on placement
- ✅ Cannot place without money
- ✅ Demo test passes

### After Task 2
- ✅ Money display in UI
- ✅ Updates correctly
- ✅ Styled consistently
- ✅ Demo test passes

### After Task 3
- ✅ Base health system working
- ✅ Game over on health = 0
- ✅ Health display in UI
- ✅ Demo test passes

### After Task 4
- ✅ Projectiles visible
- ✅ Hit effects visible
- ✅ Performance acceptable
- ✅ Demo test passes

### After Task 5
- ✅ Unit tests written
- ✅ Tests pass
- ✅ Integrated into pipeline
- ✅ Documentation complete

---

## Blockers & Dependencies

### None Currently
- All tasks are independent or have clear dependencies
- No external blockers identified
- All tools and systems ready

---

## Risk Assessment

### Task 1: Low Risk
- Pattern already established
- Services exist and work
- Well-defined requirements

### Task 2: Low Risk
- GUI is straightforward
- Update mechanism simple
- No complex interactions

### Task 3: Medium Risk
- Game over logic needs testing
- Health management important
- Edge cases to consider

### Task 4: Medium Risk
- Performance impact possible
- Visual effects subjective
- Testing important

### Task 5: Medium Risk
- Framework selection
- Test maintenance
- Integration complexity

---

## Notes

- Tasks are ordered by priority and dependencies
- Estimated times are conservative
- Actual times may vary
- Regular progress reviews recommended
- Adjust timeline based on actual progress

---

## How to Start

1. **Review this document** - Understand next tasks
2. **Read ROADMAP.md** - Understand long-term plan
3. **Read DEVELOPMENT_LOOP.md** - Understand process
4. **Start Task 1** - Begin with tower placement spending
5. **Follow the cycle** - Plan → Implement → Test → Merge

---

## Questions?

Refer to:
- `ROADMAP.md` - Long-term planning
- `DEVELOPMENT_LOOP.md` - Development process
- `CURRENT_STATE.md` - Current game state
- `ROLES.md` - Team roles
- `prompts/` - Detailed guidance
