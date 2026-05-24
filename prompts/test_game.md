# Test Game Prompt

## Task
Test a game feature to verify it works correctly.

## Instructions

### 1. Understand What to Test
- Read the feature design
- Review success criteria
- Identify test scenarios
- Note edge cases to check

### 2. Prepare Test Environment
```powershell
# Verify clean state
git status

# Build the game
.\scripts\build_place.ps1

# Verify build succeeded
ls build/game.rbxlx
```

### 3. Run Demo Test
```powershell
# Run full demo with recording
.\scripts\team_review_demo.ps1

# Or run assisted mode if focus issues
.\scripts\auto_play_assisted.ps1
```

### 4. Collect Evidence

**Video Recording:**
- Location: `logs/recordings/`
- What to look for: Feature working as designed
- Duration: Usually 30-60 seconds

**Screenshots:**
- Before test: `logs/screenshots/before_*.png`
- After test: `logs/screenshots/after_*.png`

**Roblox Logs:**
- Location: `logs/roblox_latest_markers.md`
- What to check: Service logs, errors, warnings

**Demo Report:**
- Location: `logs/demo_test_report.md`
- What to review: Status, errors, recommendations

### 5. Verify Feature Behavior

**Checklist for Each Test Scenario:**
1. Does the feature appear in the game?
2. Does it behave as designed?
3. Are there any errors in Output?
4. Does it interact correctly with other features?
5. Are there any visual glitches?
6. Does performance seem acceptable?

### 6. Check Logs

**Server Logs:**
```
[ServiceName] Message
[ServiceName] Error: ...
```

**Client Logs:**
```
[ClientName] Message
```

**Look for:**
- Service initialization messages
- Feature-specific logs
- Any error messages
- Performance warnings

### 7. Test Edge Cases

**Common Edge Cases:**
- Feature with no data
- Feature with maximum data
- Feature interaction with other systems
- Feature cleanup/removal
- Feature state persistence

### 8. Create Test Report

## Output Format

Provide a detailed test report:

```
# Test Report: [Feature Name]

## Test Summary
- **Status:** ✅ PASSED / ❌ FAILED
- **Date:** [Date]
- **Duration:** [Minutes]
- **Build:** game.rbxlx [size]

## Test Scenarios

### Scenario 1: [Description]
- **Expected:** [What should happen]
- **Actual:** [What actually happened]
- **Result:** ✅ PASS / ❌ FAIL
- **Evidence:** [Video timestamp, screenshot, log line]

### Scenario 2: [Description]
- **Expected:** [What should happen]
- **Actual:** [What actually happened]
- **Result:** ✅ PASS / ❌ FAIL
- **Evidence:** [Video timestamp, screenshot, log line]

## Log Analysis

### Server Logs
\`\`\`
[ServiceName] Initialization message
[ServiceName] Feature log
\`\`\`

### Client Logs
\`\`\`
[ClientName] Message
\`\`\`

### Errors
- [List any errors found]

## Visual Verification

### Screenshots
- Before: [Description of before state]
- After: [Description of after state]

### Video
- Duration: [seconds]
- Quality: [Good/Acceptable/Poor]
- Key moments: [Timestamps of important events]

## Performance
- **FPS:** [Observed frame rate]
- **Memory:** [If visible in logs]
- **Issues:** [Any performance problems]

## Regression Testing

### Existing Features Checked
- ✅ Enemy movement - Still working
- ✅ Tower targeting - Still working
- ✅ Reward economy - Still working
- ✅ Wave progression - Still working

### Issues Found
- [List any regressions]

## Conclusion

### Summary
[Overall assessment of feature]

### Approval
- ✅ Feature works as designed
- ✅ No regressions found
- ✅ Ready for merge

OR

- ❌ Issues found, needs fixes
- ❌ [List issues]

### Recommendations
- [Suggestions for improvement]
- [Follow-up tasks]
```

## Test Scenarios Template

For each feature, test:

1. **Basic Functionality**
   - Feature initializes correctly
   - Feature performs main action
   - Feature produces expected output

2. **Integration**
   - Feature works with other services
   - Feature respects game state
   - Feature handles dependencies

3. **Edge Cases**
   - Feature with no input
   - Feature with extreme input
   - Feature after long play time

4. **Error Handling**
   - Feature handles missing data
   - Feature handles invalid input
   - Feature recovers from errors

5. **Performance**
   - Feature doesn't cause lag
   - Feature doesn't leak memory
   - Feature scales with game size

## Log Interpretation

### Service Initialization
```
[ServiceName] Initializing
[ServiceName] Ready
```

### Feature Operation
```
[ServiceName] Action performed: [details]
[ServiceName] Result: [outcome]
```

### Errors
```
[ServiceName] Error: [description]
[ServiceName] Stack: [traceback]
```

### Warnings
```
[ServiceName] Warning: [description]
```

## Common Issues

### Feature Doesn't Appear
- Check service initialization logs
- Verify config values
- Check for errors in Output
- Verify Rojo sync completed

### Feature Doesn't Work
- Check service logs for errors
- Verify game state assumptions
- Check for missing dependencies
- Verify config values are correct

### Performance Issues
- Check for infinite loops
- Verify cleanup is happening
- Check memory usage
- Profile with Studio profiler

### Regressions
- Identify which feature broke
- Check recent changes
- Verify dependencies
- Run isolated tests

## Success Criteria

Test is complete when:
- ✅ All scenarios tested
- ✅ Evidence collected
- ✅ Logs analyzed
- ✅ Regressions checked
- ✅ Report written
- ✅ Approval given or issues documented
