# TEST_PLAN.md: Testing Strategy and Checklist

## Overview

This document defines the testing strategy for the Roblox Tower Defense prototype.

---

## Testing Levels

### Unit Testing
**Scope:** Individual functions and methods
**Responsibility:** Developer
**Tools:** Lua testing framework (future)

**Current Status:** ⏳ Not yet implemented
**Plan:** Add unit tests in Phase 4

### Integration Testing
**Scope:** Services and their interactions
**Responsibility:** Developer + Tester
**Tools:** Demo test player

**Current Status:** ✅ Implemented
**Method:** Run demo test, verify services work together

### System Testing
**Scope:** Full game loop
**Responsibility:** Tester
**Tools:** Demo test player, Roblox logs

**Current Status:** ✅ Implemented
**Method:** Run full demo, verify all features work

### Regression Testing
**Scope:** Existing features after changes
**Responsibility:** Tester
**Tools:** Demo test player, checklist

**Current Status:** ✅ Implemented
**Method:** Test all existing features after each change

---

## Test Scenarios

### Feature: Enemy Movement

**Scenario 1: Enemies spawn at correct location**
- Expected: Enemies appear near Node_1
- Verify: Check Workspace/GameRuntime/Enemies
- Pass Criteria: Enemies visible at spawn point

**Scenario 2: Enemies follow path**
- Expected: Enemies move from Node_1 to Node_7
- Verify: Watch enemies in video
- Pass Criteria: Enemies move along path smoothly

**Scenario 3: Enemies exit correctly**
- Expected: Enemies removed after reaching Node_7
- Verify: Check logs and Workspace
- Pass Criteria: Enemies disappear at exit

---

### Feature: Tower Targeting

**Scenario 1: Tower finds nearest enemy**
- Expected: Tower targets closest enemy
- Verify: Watch tower in video
- Pass Criteria: Tower attacks nearest enemy

**Scenario 2: Tower switches target**
- Expected: Tower switches to new nearest enemy
- Verify: Watch tower behavior
- Pass Criteria: Tower switches targets correctly

**Scenario 3: Tower stops when no enemies**
- Expected: Tower stops attacking
- Verify: Check logs
- Pass Criteria: Tower idle when no enemies

---

### Feature: Damage System

**Scenario 1: Enemy takes damage**
- Expected: Enemy health decreases
- Verify: Check logs
- Pass Criteria: Health attribute decreases

**Scenario 2: Enemy defeated**
- Expected: Enemy removed when health <= 0
- Verify: Check Workspace and logs
- Pass Criteria: Enemy removed correctly

**Scenario 3: Damage logged**
- Expected: Damage events logged
- Verify: Check Output logs
- Pass Criteria: Logs show damage events

---

### Feature: Reward Economy

**Scenario 1: Money awarded on kill**
- Expected: Player money increases
- Verify: Check logs
- Pass Criteria: Money increases by reward amount

**Scenario 2: Correct reward amount**
- Expected: Money matches enemy reward
- Verify: Check logs
- Pass Criteria: Reward amount correct

**Scenario 3: Money persists**
- Expected: Money doesn't reset
- Verify: Check logs
- Pass Criteria: Money accumulates correctly

---

### Feature: Wave Progression

**Scenario 1: Wave starts correctly**
- Expected: Enemies spawn for wave
- Verify: Check Workspace
- Pass Criteria: Enemies appear

**Scenario 2: Wave completes**
- Expected: Next wave starts after enemies defeated
- Verify: Check logs
- Pass Criteria: Wave progression works

**Scenario 3: Intermission works**
- Expected: Delay between waves
- Verify: Check logs
- Pass Criteria: Intermission time observed

---

### Feature: Map Generation

**Scenario 1: Map structure created**
- Expected: All folders exist
- Verify: Check Workspace/GameRuntime/Map
- Pass Criteria: All folders present

**Scenario 2: Map objects created**
- Expected: Buildings, streets, lamps exist
- Verify: Check Workspace
- Pass Criteria: Map objects visible

**Scenario 3: Path nodes created**
- Expected: Node_1 through Node_7 exist
- Verify: Check Workspace/GameRuntime/Map/PathNodes
- Pass Criteria: All nodes present

---

## Test Execution Checklist

### Pre-Test
- [ ] Working tree is clean
- [ ] Build succeeds
- [ ] No uncommitted changes
- [ ] Studio is closed
- [ ] Bridge is running (if needed)

### During Test
- [ ] Demo test runs without errors
- [ ] Video records successfully
- [ ] Screenshots capture correctly
- [ ] Logs are collected
- [ ] Game runs for full duration

### Post-Test
- [ ] Video is saved
- [ ] Screenshots are saved
- [ ] Logs are analyzed
- [ ] Report is created
- [ ] Results are documented

---

## Regression Test Checklist

After each feature implementation, verify:

### Core Systems
- [ ] RuntimeService initializes
- [ ] Services initialize in correct order
- [ ] No errors in Output logs
- [ ] Game runs without crashes

### Enemy System
- [ ] Enemies spawn correctly
- [ ] Enemies move along path
- [ ] Enemies are removed at exit
- [ ] Enemy count is correct

### Tower System
- [ ] Towers place correctly
- [ ] Towers target enemies
- [ ] Towers attack correctly
- [ ] Towers don't attack when no enemies

### Damage System
- [ ] Enemies take damage
- [ ] Enemies are defeated
- [ ] Health decreases correctly
- [ ] Damage is logged

### Economy System
- [ ] Money starts at correct amount
- [ ] Money increases on kill
- [ ] Money amount is correct
- [ ] Money persists

### Wave System
- [ ] Waves start correctly
- [ ] Waves progress correctly
- [ ] Intermission works
- [ ] All waves complete

### Map System
- [ ] Map generates correctly
- [ ] All folders exist
- [ ] All objects created
- [ ] Path nodes exist

---

## Log Analysis Checklist

### Server Logs
- [ ] No error messages
- [ ] All services initialized
- [ ] Feature logs present
- [ ] Expected messages appear

### Client Logs
- [ ] No error messages
- [ ] Client initialized
- [ ] No unexpected warnings

### Performance
- [ ] No lag or stuttering
- [ ] FPS stable at 60
- [ ] No memory warnings
- [ ] No timeout errors

---

## Test Report Template

```
# Test Report: [Feature Name]

## Summary
- Status: ✅ PASSED / ❌ FAILED
- Date: [Date]
- Duration: [Minutes]
- Tester: [Name]

## Test Scenarios
- Scenario 1: ✅ PASS / ❌ FAIL
- Scenario 2: ✅ PASS / ❌ FAIL
- Scenario 3: ✅ PASS / ❌ FAIL

## Regression Tests
- Enemy Movement: ✅ PASS
- Tower Targeting: ✅ PASS
- Damage System: ✅ PASS
- Economy System: ✅ PASS
- Wave Progression: ✅ PASS
- Map Generation: ✅ PASS

## Issues Found
- [Issue 1]
- [Issue 2]

## Logs Analysis
- No errors found
- All services initialized
- Performance acceptable

## Approval
✅ APPROVED - Ready for merge

## Recommendations
- [Suggestion 1]
- [Suggestion 2]
```

---

## Known Issues & Workarounds

### Windows Focus Issue
**Issue:** Windows doesn't keep foreground on Roblox Studio
**Workaround:** Use assisted mode and manually click window
**Status:** Mitigated

### Build Time
**Issue:** Build takes 2-3 seconds
**Workaround:** None needed, acceptable
**Status:** Acceptable

---

## Performance Baselines

### Build Time
- Target: < 5 seconds
- Current: ~2-3 seconds
- Status: ✅ Good

### Game Load Time
- Target: < 10 seconds
- Current: ~5-10 seconds
- Status: ✅ Good

### Demo Test Duration
- Target: < 2 minutes
- Current: ~1-1.5 minutes
- Status: ✅ Good

### FPS
- Target: 60 FPS
- Current: 60 FPS
- Status: ✅ Good

---

## Test Coverage

### Current Coverage
- ✅ Enemy movement
- ✅ Tower targeting
- ✅ Damage system
- ✅ Reward economy
- ✅ Wave progression
- ✅ Map generation
- ⏳ Tower placement spending (not implemented)
- ⏳ UI money display (not implemented)
- ⏳ Base health system (not implemented)

### Target Coverage
- ✅ All implemented features
- ✅ All edge cases
- ✅ All error conditions
- ✅ Performance under load

---

## Test Automation

### Current Automation
- ✅ Build pipeline (Rojo)
- ✅ Demo test player
- ✅ Video recording
- ✅ Screenshot capture
- ✅ Log collection

### Future Automation
- ⏳ Unit test framework
- ⏳ Automated regression tests
- ⏳ Performance profiling
- ⏳ Load testing

---

## Test Environment

### Hardware
- Windows 11 Pro
- Roblox Studio (latest)
- Python 3.x
- PowerShell 5+

### Software
- Rojo (build system)
- gh (GitHub CLI)
- Studio Operator v4

### Network
- Local development
- No internet required
- Bridge server on localhost

---

## Test Frequency

### Per Feature
- Design review: After planning
- Code review: After implementation
- Demo test: Before merge
- Regression test: Before merge

### Per Release
- Full regression test: Before release
- Performance test: Before release
- Load test: Before release

### Continuous
- Build verification: Every commit
- Syntax check: Every edit
- Log analysis: Every test

---

## Success Criteria

### Test is Successful When
- ✅ All scenarios pass
- ✅ No regressions found
- ✅ Logs are clean
- ✅ Performance acceptable
- ✅ Feature works as designed

### Feature is Ready When
- ✅ All tests pass
- ✅ Code review approved
- ✅ No known issues
- ✅ Documentation complete
- ✅ Ready for merge

---

## Questions?

Refer to:
- `prompts/test_game.md` - Testing guide
- `DEVELOPMENT_LOOP.md` - Development cycle
- `CURRENT_STATE.md` - Current game state
