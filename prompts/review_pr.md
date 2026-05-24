# Review PR Prompt

## Task
Review a Pull Request for the Roblox Tower Defense prototype.

## Instructions

### 1. Understand the PR
```powershell
# View PR details
gh pr view <PR_NUMBER>

# View PR diff
gh pr diff <PR_NUMBER>
```

- What feature does it add?
- What files does it change?
- What is the description?
- Are there any related issues?

### 2. Check PR Status
```powershell
# View PR checks
gh pr checks <PR_NUMBER>
```

- Do all checks pass?
- Are there any failing tests?
- Are there any review comments?

### 3. Review Code Changes

For each changed file:
1. **Understand the change**
   - What was changed?
   - Why was it changed?
   - Does it match the design?

2. **Check code quality**
   - Does it follow project patterns?
   - Is it well-commented?
   - Are there any obvious bugs?
   - Is error handling adequate?

3. **Verify correctness**
   - Does it implement the design?
   - Are all requirements met?
   - Are edge cases handled?
   - Are dependencies correct?

### 4. Test the Feature

**Build and Test:**
```powershell
# Checkout PR branch
git fetch origin pull/<PR_NUMBER>/head:pr-<PR_NUMBER>
git checkout pr-<PR_NUMBER>

# Build
.\scripts\build_place.ps1

# Run demo test
.\scripts\team_review_demo.ps1
```

**Verify:**
- ✅ Build succeeds
- ✅ Demo runs without errors
- ✅ Feature works as designed
- ✅ No regressions in other features

### 5. Check for Regressions

**Test Existing Features:**
- Enemy movement along path
- Tower targeting and damage
- Reward economy
- Wave progression
- Map generation
- Bridge connectivity

**Look for:**
- Crashes or errors
- Missing features
- Changed behavior
- Performance issues

### 6. Review Logs

**Roblox Output Logs:**
- Location: `logs/roblox_latest_markers.md`
- Look for: Errors, warnings, unexpected behavior

**Demo Report:**
- Location: `logs/demo_test_report.md`
- Review: Status, findings, recommendations

### 7. Provide Feedback

## Output Format

Provide a detailed PR review:

```
# PR Review: [PR Title]

## PR Summary
- **Number:** #[N]
- **Author:** [Name]
- **Branch:** [Branch name]
- **Status:** ✅ READY TO MERGE / ⏳ NEEDS CHANGES / ❌ BLOCKED

## Code Review

### Changed Files
- `src/server/services/MyService.lua` - [Assessment]
- `src/shared/configs/MyConfig.lua` - [Assessment]

### Code Quality
- ✅ Follows project patterns
- ✅ Well-commented
- ✅ Error handling adequate
- ✅ No obvious bugs

### Correctness
- ✅ Implements design correctly
- ✅ All requirements met
- ✅ Edge cases handled
- ✅ Dependencies correct

## Test Results

### Build
- ✅ Build succeeds
- ✅ No Lua errors
- ✅ All imports correct

### Feature Testing
- ✅ Feature works as designed
- ✅ All scenarios pass
- ✅ Performance acceptable

### Regression Testing
- ✅ Enemy movement works
- ✅ Tower targeting works
- ✅ Reward economy works
- ✅ Wave progression works
- ✅ Map generation works

## Logs Analysis

### Errors
- [List any errors found]

### Warnings
- [List any warnings]

### Performance
- [Note any performance issues]

## Approval

### Recommendation
- ✅ APPROVED - Ready to merge
- ⏳ CONDITIONAL - Needs minor fixes
- ❌ REJECTED - Major issues found

### Comments
- [Detailed feedback]

### Required Changes
- [List any required changes]

### Suggestions
- [List optional improvements]

## Merge Readiness

- ✅ All checks pass
- ✅ Code review complete
- ✅ Tests pass
- ✅ No regressions
- ✅ Ready for safe merge

### Merge Command
\`\`\`powershell
.\scripts\pr_safe_merge.ps1 -PrNumber <N>
\`\`\`
```

## Code Review Checklist

### Design Compliance
- ✅ Implements approved design
- ✅ No scope creep
- ✅ Follows architecture
- ✅ Respects constraints

### Code Quality
- ✅ Follows naming conventions
- ✅ Proper indentation
- ✅ Clear variable names
- ✅ Adequate comments
- ✅ No dead code
- ✅ No debug code left in

### Error Handling
- ✅ Validates inputs
- ✅ Handles edge cases
- ✅ Provides error messages
- ✅ Doesn't crash on bad data

### Performance
- ✅ No infinite loops
- ✅ Proper cleanup
- ✅ No memory leaks
- ✅ Reasonable complexity

### Dependencies
- ✅ Correct imports
- ✅ No circular dependencies
- ✅ Proper initialization order
- ✅ Services initialized correctly

## Test Verification Checklist

### Build
- ✅ Rojo build succeeds
- ✅ No Lua syntax errors
- ✅ No import errors
- ✅ Build artifact created

### Feature
- ✅ Feature initializes
- ✅ Feature performs main action
- ✅ Feature produces correct output
- ✅ Feature logs appropriately

### Integration
- ✅ Works with other services
- ✅ Respects game state
- ✅ Handles dependencies
- ✅ No conflicts with existing code

### Regression
- ✅ All existing features work
- ✅ No new errors
- ✅ No performance degradation
- ✅ No broken functionality

## Common Issues to Look For

### Code Issues
- Hardcoded values instead of configs
- Missing error handling
- Inconsistent naming
- Commented-out code
- Debug print statements

### Design Issues
- Doesn't match approved design
- Scope creep beyond design
- Missing required functionality
- Violates architecture

### Test Issues
- Feature doesn't work
- Regressions in other features
- Errors in logs
- Performance problems

## Approval Criteria

PR is approved when:
- ✅ Code review passes
- ✅ All checks pass
- ✅ Feature works correctly
- ✅ No regressions found
- ✅ Logs are clean
- ✅ Performance is acceptable
- ✅ Ready for safe merge

## Success Criteria

Review is complete when:
- ✅ Code reviewed
- ✅ Tests run
- ✅ Logs analyzed
- ✅ Approval given
- ✅ Feedback provided
