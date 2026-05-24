# ROADMAP.md: 6-Month Feature Roadmap

## Overview

This document outlines the planned features and timeline for the Roblox Tower Defense prototype over the next 6 months.

**Current Phase:** Foundation Complete (May 2026)
**Next Phase:** Core Features (May-June 2026)

---

## Phase 1: Foundation (✅ Complete)
**Timeline:** April - May 2026
**Status:** ✅ DONE

### Completed Features
- ✅ Rojo build pipeline
- ✅ Studio Operator v4
- ✅ Enemy movement system
- ✅ Tower targeting and damage
- ✅ Reward economy
- ✅ Wave progression
- ✅ Backlund Fog District map
- ✅ Demo test player
- ✅ Safe PR manager

### Outcome
- Foundation is solid
- All core systems working
- Ready for feature development
- Build and test pipelines verified

---

## Phase 2: Core Features (⏳ In Progress)
**Timeline:** May - June 2026
**Status:** ⏳ IN PROGRESS

### Feature 1: Tower Placement Spending
**Description:** Deduct money when placing towers
**Effort:** 4-8 hours
**Priority:** High
**Dependencies:** EconomyService ✅, TowerService ✅
**Success Criteria:**
- ✅ Tower costs defined in config
- ✅ Money deducted on placement
- ✅ Cannot place if insufficient funds
- ✅ UI shows cost before placement

### Feature 2: UI Money Display
**Description:** Show player money in GUI
**Effort:** 4-8 hours
**Priority:** High
**Dependencies:** EconomyService ✅, StarterGui
**Success Criteria:**
- ✅ Money display in corner of screen
- ✅ Updates when money changes
- ✅ Shows current and max money
- ✅ Styled consistently

### Feature 3: Base Health/Lives System
**Description:** Player loses lives when enemies reach exit
**Effort:** 4-8 hours
**Priority:** High
**Dependencies:** EnemyService ✅, WaveService ✅
**Success Criteria:**
- ✅ Base starts with health
- ✅ Enemies deal damage on exit
- ✅ Game over when health reaches 0
- ✅ Health display in UI

### Feature 4: Projectile Visuals
**Description:** Improve visual effects for attacks
**Effort:** 4-8 hours
**Priority:** Medium
**Dependencies:** TowerService ✅
**Success Criteria:**
- ✅ Projectiles visible in flight
- ✅ Hit effects visible
- ✅ Consistent with tower type
- ✅ Performance acceptable

### Timeline
- Week 1-2: Tower Placement Spending
- Week 2-3: UI Money Display
- Week 3-4: Base Health System
- Week 4-5: Projectile Visuals

---

## Phase 3: Advanced Features (⏳ Planned)
**Timeline:** June - July 2026
**Status:** ⏳ PLANNED

### Feature 1: Gacha Unit System
**Description:** Implement unit gacha (Lord of the Mysteries theme)
**Effort:** 16-24 hours
**Priority:** High
**Dependencies:** Phase 2 complete
**Subtasks:**
- Define unit types and rarities
- Create gacha mechanics
- Implement unit placement
- Add unit upgrade system
- Create UI for gacha

### Feature 2: Unit Upgrade System
**Description:** Upgrade units with money
**Effort:** 8-12 hours
**Priority:** High
**Dependencies:** Gacha system
**Subtasks:**
- Define upgrade paths
- Implement upgrade mechanics
- Add cost scaling
- Create upgrade UI

### Feature 3: Advanced Towers
**Description:** Add more tower types
**Effort:** 8-12 hours
**Priority:** Medium
**Dependencies:** Phase 2 complete
**Subtasks:**
- Design tower types
- Implement tower mechanics
- Add tower configs
- Balance tower costs

### Timeline
- Week 1-3: Gacha Unit System
- Week 3-4: Unit Upgrade System
- Week 4-5: Advanced Towers

---

## Phase 4: Polish & Optimization (⏳ Planned)
**Timeline:** July - August 2026
**Status:** ⏳ PLANNED

### Feature 1: Save/Load System
**Description:** Persist game state
**Effort:** 12-16 hours
**Priority:** High
**Dependencies:** Phase 3 complete
**Subtasks:**
- Design save format
- Implement save mechanics
- Implement load mechanics
- Add save UI

### Feature 2: Sound & Music
**Description:** Add audio to game
**Effort:** 8-12 hours
**Priority:** Medium
**Dependencies:** Phase 2 complete
**Subtasks:**
- Find/create sound effects
- Find/create music
- Implement audio system
- Add audio settings

### Feature 3: Performance Optimization
**Description:** Optimize game performance
**Effort:** 8-12 hours
**Priority:** Medium
**Dependencies:** All phases
**Subtasks:**
- Profile game
- Identify bottlenecks
- Optimize hot paths
- Reduce memory usage

### Timeline
- Week 1-3: Save/Load System
- Week 3-4: Sound & Music
- Week 4-5: Performance Optimization

---

## Phase 5: Content & Balance (⏳ Planned)
**Timeline:** August - September 2026
**Status:** ⏳ PLANNED

### Feature 1: More Waves
**Description:** Add more waves and difficulty scaling
**Effort:** 4-8 hours
**Priority:** Medium
**Dependencies:** Phase 2 complete
**Subtasks:**
- Design wave progression
- Implement difficulty scaling
- Balance enemy stats
- Create wave configs

### Feature 2: Map Variants
**Description:** Add more maps
**Effort:** 12-16 hours
**Priority:** Medium
**Dependencies:** Phase 2 complete
**Subtasks:**
- Design map layouts
- Implement map builder
- Create path variants
- Balance map difficulty

### Feature 3: Achievements & Leaderboards
**Description:** Add progression and competition
**Effort:** 8-12 hours
**Priority:** Low
**Dependencies:** Phase 4 complete
**Subtasks:**
- Design achievements
- Implement achievement system
- Create leaderboard UI
- Add score tracking

### Timeline
- Week 1-2: More Waves
- Week 2-4: Map Variants
- Week 4-5: Achievements & Leaderboards

---

## Phase 6: Release Preparation (⏳ Planned)
**Timeline:** September - October 2026
**Status:** ⏳ PLANNED

### Activities
- Bug fixes and polish
- Performance optimization
- Documentation completion
- User testing
- Marketing preparation
- Release planning

### Success Criteria
- ✅ All features complete
- ✅ No known bugs
- ✅ Performance acceptable
- ✅ Documentation complete
- ✅ Ready for public release

---

## Feature Priority Matrix

### High Priority (Must Have)
1. Tower Placement Spending
2. UI Money Display
3. Base Health System
4. Gacha Unit System
5. Save/Load System

### Medium Priority (Should Have)
1. Projectile Visuals
2. Unit Upgrade System
3. Advanced Towers
4. Sound & Music
5. More Waves
6. Map Variants

### Low Priority (Nice to Have)
1. Performance Optimization
2. Achievements & Leaderboards
3. Advanced UI
4. Multiplayer (future)
5. Mobile Support (future)

---

## Effort Estimation

### Total Effort by Phase
- Phase 1: ✅ ~80 hours (complete)
- Phase 2: ⏳ ~32 hours (in progress)
- Phase 3: ⏳ ~40 hours (planned)
- Phase 4: ⏳ ~32 hours (planned)
- Phase 5: ⏳ ~24 hours (planned)
- Phase 6: ⏳ ~40 hours (planned)

**Total:** ~248 hours

### Effort by Role
- **Architect:** ~40 hours (design and planning)
- **Developer:** ~160 hours (implementation)
- **Tester:** ~30 hours (testing and verification)
- **DevOps:** ~18 hours (build and deployment)

---

## Risk Assessment

### High Risk
- **Gacha system complexity** - Mitigation: Start simple, iterate
- **Performance with many units** - Mitigation: Profile and optimize early
- **Save/load system bugs** - Mitigation: Extensive testing

### Medium Risk
- **Audio licensing** - Mitigation: Use royalty-free assets
- **Map design balance** - Mitigation: Playtest extensively
- **UI complexity** - Mitigation: Keep UI simple initially

### Low Risk
- **Basic features** - Well-understood patterns
- **Existing systems** - Already proven to work
- **Build pipeline** - Already stable

---

## Dependencies

### Feature Dependencies
```
Foundation (✅)
    ├─ Tower Placement Spending
    ├─ UI Money Display
    ├─ Base Health System
    └─ Projectile Visuals
        ├─ Gacha Unit System
        │   └─ Unit Upgrade System
        └─ Advanced Towers
            ├─ Save/Load System
            ├─ Sound & Music
            └─ Performance Optimization
                ├─ More Waves
                ├─ Map Variants
                └─ Achievements & Leaderboards
```

### External Dependencies
- Rojo (build system)
- Roblox Studio
- Python 3.x
- GitHub CLI

---

## Milestones

### Milestone 1: Foundation Complete ✅
**Date:** May 2026
**Status:** ✅ COMPLETE
**Features:** All foundation features

### Milestone 2: Core Features Complete ⏳
**Date:** June 2026
**Status:** ⏳ IN PROGRESS
**Features:** Tower spending, UI, base health, projectiles

### Milestone 3: Advanced Features Complete
**Date:** July 2026
**Status:** ⏳ PLANNED
**Features:** Gacha, upgrades, advanced towers

### Milestone 4: Polished & Optimized
**Date:** August 2026
**Status:** ⏳ PLANNED
**Features:** Save/load, sound, optimization

### Milestone 5: Content Complete
**Date:** September 2026
**Status:** ⏳ PLANNED
**Features:** More waves, maps, achievements

### Milestone 6: Ready for Release
**Date:** October 2026
**Status:** ⏳ PLANNED
**Features:** All features, polished, documented

---

## Success Metrics

### By Phase
- **Phase 1:** Foundation working, all systems verified
- **Phase 2:** Core gameplay loop complete
- **Phase 3:** Advanced mechanics working
- **Phase 4:** Game polished and optimized
- **Phase 5:** Content rich and balanced
- **Phase 6:** Ready for public release

### Overall
- ✅ All planned features implemented
- ✅ No critical bugs
- ✅ Performance acceptable
- ✅ User satisfaction high
- ✅ Ready for release

---

## Notes

- Timeline is estimated and may shift
- Priorities may change based on feedback
- New features may be added
- Some features may be deferred
- Regular reviews recommended

---

## Questions?

Refer to:
- `CURRENT_STATE.md` - Current game state
- `ROLES.md` - Team roles
- `DEVELOPMENT_LOOP.md` - Development process
