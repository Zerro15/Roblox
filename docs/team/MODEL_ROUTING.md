# MODEL_ROUTING.md: AI Model Selection Policy

## Overview

This document defines how to select the appropriate AI model or Codex profile for different types of development tasks.

**Goal:** Use the right tool for the job - avoid wasting expensive models on simple tasks, and ensure critical tasks get sufficient reasoning capacity.

---

## Model Routing Levels

### Level 1: Quick ⚡

**Recommended Claude Model:** `haiku`
**Recommended Codex Profile:** `quick`
**Cost:** Lowest
**Speed:** Fastest
**Reasoning:** Basic

**Use for:**
- Status checks and reporting
- Documentation updates (README, comments)
- Prompt library management
- Simple scripts (PowerShell, bash)
- Dry-run builds
- Team status summaries
- Task planning from roadmap
- Log summarization
- Simple refactoring

**Examples:**
- `Update README.md with new section`
- `Check team status`
- `List available prompts`
- `Summarize demo test results`
- `Create PowerShell wrapper script`

**Safety:** ✅ Safe for non-critical tasks

---

### Level 2: Code 💻

**Recommended Claude Model:** `sonnet`
**Recommended Codex Profile:** `standard` or `code`
**Cost:** Medium
**Speed:** Medium
**Reasoning:** Strong

**Use for:**
- Roblox Lua implementation
- Python tool development
- PowerShell automation scripts
- Bug fixes in game code
- Normal PR reviews
- Small refactoring (single file)
- Feature implementation (single service)
- Test writing
- Config updates

**Examples:**
- `Add tower placement spending feature`
- `Implement UI money display`
- `Fix enemy movement bug`
- `Create new service for health system`
- `Write unit tests for EconomyService`

**Safety:** ✅ Safe for code changes with clear scope

---

### Level 3: Deep 🧠

**Recommended Claude Model:** `opus` or `opusplan`
**Recommended Codex Profile:** `deep`
**Cost:** Highest
**Speed:** Slowest
**Reasoning:** Maximum

**Use for:**
- Architecture and system design
- Complex debugging (race conditions, subtle bugs)
- Cross-file refactoring (affects multiple services)
- PR manager or process manager changes
- Auto-merge safety verification
- Security and abuse prevention
- Video/log analysis with unclear cause
- Major version upgrades
- Performance optimization (complex)
- Merge conflict resolution

**Examples:**
- `Design gacha unit system architecture`
- `Debug race condition in wave progression`
- `Refactor service initialization system`
- `Fix PR safe merge manager bug`
- `Analyze why demo test failed mysteriously`

**Safety:** ⚠️ Required for risky operations

---

### Level 4: Verify ✓

**Recommended Claude Model:** `haiku` or `sonnet`
**Recommended Codex Profile:** `verify`
**Cost:** Low to Medium
**Speed:** Fast to Medium
**Reasoning:** Focused

**Use for:**
- Build verification and checks
- Log review and analysis
- Demo report review
- PR check verification
- Smoke tests
- Regression detection
- Test result analysis

**Examples:**
- `Verify build succeeded`
- `Review Roblox logs for errors`
- `Check demo test report`
- `Verify PR checks passed`
- `Detect regressions in test results`

**Safety:** ✅ Safe for verification tasks

---

## Decision Tree

```
Task received
    ↓
Is it documentation/README/status?
    ├─ YES → QUICK (haiku)
    └─ NO ↓
Is it code implementation/feature/bugfix?
    ├─ YES (single service/file) → CODE (sonnet)
    ├─ YES (multiple services) → CODE or DEEP
    └─ NO ↓
Is it verification/testing/review?
    ├─ YES → VERIFY (haiku/sonnet)
    └─ NO ↓
Is it architecture/security/merge/debug?
    ├─ YES → DEEP (opus/opusplan)
    └─ NO ↓
Is it risky or unclear?
    ├─ YES → DEEP (opus/opusplan)
    └─ NO → CODE (sonnet)
```

---

## Rules

### Always Use Quick For:
- ✅ README and documentation
- ✅ Status checks
- ✅ Prompt library management
- ✅ Simple scripts
- ✅ Summarization tasks

### Never Use Quick For:
- ❌ Risky merge operations
- ❌ Security-related changes
- ❌ Hard debugging
- ❌ Architecture decisions
- ❌ PR manager changes

### Always Use Code For:
- ✅ Game feature implementation
- ✅ Single-service changes
- ✅ Bug fixes with clear cause
- ✅ Normal PR reviews
- ✅ Test writing

### Always Use Deep For:
- ✅ PR manager or process manager changes
- ✅ Auto-merge safety verification
- ✅ Architecture design
- ✅ Race condition debugging
- ✅ Cross-service refactoring
- ✅ Security reviews

### When in Doubt:
- Choose the safer (more powerful) level
- But don't use Deep by default
- Prefer Code over Deep unless clearly needed
- Ask for clarification if task is ambiguous

---

## Model Capabilities

### Haiku
- Fast responses
- Good for simple tasks
- Limited reasoning
- Perfect for status/docs
- **Cost:** ~1/10 of Opus

### Sonnet
- Balanced speed and reasoning
- Good for code implementation
- Can handle moderate complexity
- Good for PR reviews
- **Cost:** ~1/3 of Opus

### Opus / OpusPlan
- Maximum reasoning capacity
- Slow but thorough
- Handles complex problems
- Perfect for architecture
- **Cost:** Baseline (100%)

---

## Examples

### Example 1: Update README
```
Task: "Update README.md with model routing section"
Analysis:
  - Documentation only
  - No code changes
  - No risk
Decision: QUICK (haiku)
Command: claude --model haiku
```

### Example 2: Add Tower Spending
```
Task: "Add tower placement spending feature"
Analysis:
  - Code implementation
  - Single service (TowerService)
  - Clear requirements
  - Moderate complexity
Decision: CODE (sonnet)
Command: claude --model sonnet
```

### Example 3: Fix PR Manager Bug
```
Task: "Fix PR safe merge manager bug"
Analysis:
  - PR manager change (risky)
  - Affects merge safety
  - Complex logic
  - High risk
Decision: DEEP (opus/opusplan)
Command: claude --model opusplan
```

### Example 4: Review Demo Logs
```
Task: "Review demo test logs for errors"
Analysis:
  - Verification task
  - Log analysis
  - No code changes
  - Clear scope
Decision: VERIFY (sonnet)
Command: claude --model sonnet
```

### Example 5: Design Gacha System
```
Task: "Design gacha unit system architecture"
Analysis:
  - Architecture design
  - Complex system
  - Multiple services
  - Strategic decision
Decision: DEEP (opus/opusplan)
Command: claude --model opusplan
```

---

## Switching Models Mid-Task

### When to Switch:
- Task complexity increases unexpectedly
- Original model insufficient for problem
- New sub-task requires different level
- Risk assessment changes

### How to Switch:
```
Claude: "This task requires deeper reasoning than initially thought.
Switching to opusplan for architecture review."

/model opusplan
```

### Document the Switch:
- Note in commit message
- Explain why in PR description
- Update task documentation

---

## Cost Optimization

### Estimate Before Starting
```
Quick task: 1-2 min, haiku
Code task: 5-15 min, sonnet
Deep task: 15-30 min, opus
```

### Batch Similar Tasks
- Group Quick tasks together
- Group Code tasks together
- Schedule Deep tasks separately

### Monitor Usage
- Track model usage per task
- Identify patterns
- Optimize future decisions

---

## Integration with Development Cycle

### Phase 1: Planning
- **Model:** Quick or Code
- **Reason:** Design can be simple or complex
- **Decision:** Use Quick for roadmap, Code for architecture

### Phase 2: Implementation
- **Model:** Code (primary)
- **Reason:** Code implementation is standard
- **Decision:** Use Code unless cross-service

### Phase 3: Testing
- **Model:** Verify (haiku/sonnet)
- **Reason:** Verification is focused
- **Decision:** Use Verify for log analysis

### Phase 4: Merge
- **Model:** Deep (if risky) or Code
- **Reason:** Merge safety is critical
- **Decision:** Use Deep for PR manager, Code for normal merge

---

## Codex CLI Integration

When using Codex CLI:

1. **Determine task mode** before starting
2. **Select appropriate profile** (quick/code/deep/verify)
3. **Codex will recommend** if current model is insufficient
4. **Explicit notification** if switching models
5. **No silent model changes** during task execution

### Codex Recommendation Format:
```
Task: "Fix PR safe merge manager bug"
Current profile: code
Recommended profile: deep
Reason: PR manager changes require deep reasoning for safety
Recommendation: Switch to deep profile? (y/n)
```

---

## FAQ

### Q: Can I use Quick for code?
**A:** Only for very simple scripts or documentation. Avoid for game code.

### Q: When should I use Sonnet vs Opus?
**A:** Use Sonnet for normal code. Use Opus for architecture, complex bugs, or risky changes.

### Q: What if I'm not sure?
**A:** Choose the safer level. It's better to use Opus unnecessarily than Quick insufficiently.

### Q: Can I use Quick for PR review?
**A:** Only for simple PRs. Use Code or Deep for complex changes.

### Q: How do I know if a task is risky?
**A:** If it affects PR manager, merge logic, git history, or multiple services - it's risky. Use Deep.

---

## Monitoring and Adjustment

### Track These Metrics:
- Model usage per task type
- Task success rate by model
- Time spent per model
- Cost per task type

### Adjust When:
- Quick tasks fail (upgrade to Code)
- Code tasks take too long (might need Deep)
- Deep tasks are overkill (downgrade to Code)
- Patterns emerge in task complexity

---

## Notes

- This policy is flexible and can be adjusted
- Err on the side of caution for risky tasks
- Document model choices in PR descriptions
- Review and update quarterly
- Share learnings with team
