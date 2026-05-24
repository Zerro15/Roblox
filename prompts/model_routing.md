# Model Routing Prompt

## Task

Analyze a development task and recommend the appropriate AI model or Codex profile.

## Input

Provide the following information about the task:

1. **Task Title** - What needs to be done?
2. **Affected Files** - Which files will be modified?
3. **Risk Level** - Low / Medium / High / Critical
4. **Expected Operations** - What will the task do?
5. **Code Changes** - Yes / No
6. **Merge Required** - Yes / No
7. **Roblox Demo** - Yes / No

## Analysis Framework

### Step 1: Categorize the Task
- Is it documentation/status? → QUICK
- Is it code implementation? → CODE
- Is it verification/testing? → VERIFY
- Is it architecture/security/risky? → DEEP

### Step 2: Check Risk Level
- Low risk + simple scope → QUICK or CODE
- Medium risk + moderate scope → CODE
- High/Critical risk → DEEP
- Risky operations (merge, PR manager) → DEEP

### Step 3: Check Affected Scope
- Single file/service → CODE
- Multiple services → CODE or DEEP
- Core systems (PR manager, process manager) → DEEP
- Architecture changes → DEEP

### Step 4: Check Operations
- Read-only (status, review) → QUICK or VERIFY
- Code changes (implementation) → CODE
- Merge operations → DEEP
- Security/safety critical → DEEP

### Step 5: Make Recommendation
Based on above analysis, recommend:
- **Mode:** quick / code / deep / verify
- **Claude Model:** haiku / sonnet / opus / opusplan
- **Codex Profile:** quick / code / deep / verify
- **Reason:** Explain why this mode is recommended
- **Safe Command:** How to start this task

## Output Format

```
# Model Routing Analysis

## Task Summary
- Title: [Task title]
- Risk Level: [Low/Medium/High/Critical]
- Scope: [Single file/service/multiple/system-wide]
- Operations: [Read-only/Code/Merge/Security]

## Analysis
- Documentation? [Yes/No]
- Code changes? [Yes/No]
- Risky operations? [Yes/No]
- Multiple services? [Yes/No]
- Affects core systems? [Yes/No]

## Recommendation

**Recommended Mode:** [quick/code/deep/verify]

**Claude Model:** [haiku/sonnet/opus/opusplan]

**Codex Profile:** [quick/code/deep/verify]

**Reason:**
[Explain the decision based on analysis]

## Safe Commands

### To Start with Claude:
\`\`\`powershell
claude --model [model]
\`\`\`

### To Start with Codex CLI:
\`\`\`bash
codex --profile [profile]
\`\`\`

### To Get Recommendation:
\`\`\`powershell
.\scripts\model_recommend.ps1 -Task "[task title]"
\`\`\`

## Warnings (if any)
- [Any warnings or special considerations]

## Next Steps
1. [First step]
2. [Second step]
3. [Third step]
```

## Examples

### Example 1: Simple Documentation

**Input:**
- Task: "Update README.md with model routing section"
- Affected Files: README.md
- Risk Level: Low
- Code Changes: No
- Merge Required: No
- Roblox Demo: No

**Analysis:**
- Documentation only ✓
- No code changes ✓
- No risk ✓
- Read-only operation ✓

**Output:**
```
Recommended Mode: quick
Claude Model: haiku
Codex Profile: quick
Reason: Documentation update with no code changes or risk
Safe Command: claude --model haiku
```

---

### Example 2: Feature Implementation

**Input:**
- Task: "Add tower placement spending feature"
- Affected Files: TowerService.lua, EconomyService.lua, TowerConfig.lua
- Risk Level: Medium
- Code Changes: Yes
- Merge Required: Yes
- Roblox Demo: Yes

**Analysis:**
- Code implementation ✓
- Multiple files but single service ✓
- Medium risk ✓
- Merge required ✓
- Demo needed ✓

**Output:**
```
Recommended Mode: code
Claude Model: sonnet
Codex Profile: code
Reason: Feature implementation with moderate complexity and demo testing
Safe Command: claude --model sonnet
```

---

### Example 3: PR Manager Bug Fix

**Input:**
- Task: "Fix PR safe merge manager bug"
- Affected Files: pr_manager.py, studio_flow.py
- Risk Level: Critical
- Code Changes: Yes
- Merge Required: Yes
- Roblox Demo: No

**Analysis:**
- Code implementation ✓
- Affects PR manager (core system) ✓
- Critical risk ✓
- Merge safety critical ✓
- Complex logic ✓

**Output:**
```
Recommended Mode: deep
Claude Model: opusplan
Codex Profile: deep
Reason: PR manager changes are critical for merge safety and require deep reasoning
Safe Command: claude --model opusplan
```

---

### Example 4: Log Analysis

**Input:**
- Task: "Review demo test logs for errors"
- Affected Files: logs/demo_test_report.md, logs/roblox_latest_markers.md
- Risk Level: Low
- Code Changes: No
- Merge Required: No
- Roblox Demo: No

**Analysis:**
- Verification task ✓
- Log analysis ✓
- No code changes ✓
- No risk ✓
- Read-only operation ✓

**Output:**
```
Recommended Mode: verify
Claude Model: sonnet
Codex Profile: verify
Reason: Log analysis and verification task with focused scope
Safe Command: claude --model sonnet
```

---

### Example 5: Architecture Design

**Input:**
- Task: "Design gacha unit system architecture"
- Affected Files: Multiple services (future)
- Risk Level: High
- Code Changes: No (design only)
- Merge Required: No
- Roblox Demo: No

**Analysis:**
- Architecture design ✓
- Complex system ✓
- High risk (strategic) ✓
- Multiple services affected ✓
- Requires deep reasoning ✓

**Output:**
```
Recommended Mode: deep
Claude Model: opusplan
Codex Profile: deep
Reason: Architecture design requires deep reasoning for complex system
Safe Command: claude --model opusplan
```

## Decision Rules

### Always Quick:
- README/documentation
- Status checks
- Simple scripts
- Summarization

### Always Code:
- Feature implementation
- Bug fixes (clear cause)
- Single-service changes
- Test writing

### Always Deep:
- PR manager changes
- Architecture design
- Complex debugging
- Security reviews
- Risky operations

### Always Verify:
- Log analysis
- Build checks
- Test reviews
- Regression detection

## Tips

1. **Be honest about risk** - If unsure, choose safer level
2. **Consider scope** - Multiple services = higher level
3. **Think about safety** - Merge operations need Deep
4. **Document decisions** - Explain in PR description
5. **Learn from patterns** - Track what works

## Success Criteria

Routing is successful when:
- ✅ Task completed efficiently
- ✅ Model was appropriate for complexity
- ✅ No rework needed
- ✅ Cost was reasonable
- ✅ Safety was maintained
