# Design Feature Prompt

## Task
Design a new game feature for the Roblox Tower Defense prototype.

## Instructions

### 1. Understand Requirements
- What problem does this feature solve?
- What is the user-facing behavior?
- How does it fit into the game loop?
- What is the priority and timeline?

### 2. Review Current State
- Read `docs/team/CURRENT_STATE.md` for game state
- Check `docs/team/ROADMAP.md` for context
- Identify related existing features
- Note any dependencies or constraints

### 3. Analyze Existing Patterns
- Review relevant services in `src/server/services/`
- Check related configs in `src/shared/configs/`
- Identify code patterns and conventions
- Note how similar features are implemented

### 4. Design Architecture
- What new services are needed?
- What configs need to be added/modified?
- What existing services need changes?
- How do components interact?

### 5. Identify Affected Files
- List all files that will be modified
- List all files that will be created
- Note any breaking changes
- Identify backward compatibility concerns

### 6. Plan Implementation Steps
- Break feature into logical steps
- Identify dependencies between steps
- Estimate effort for each step
- Note any risky or complex parts

### 7. Define Success Criteria
- What does "done" look like?
- How will we verify the feature works?
- What tests are needed?
- What logs should we check?

### 8. Identify Risks
- What could go wrong?
- What existing features could break?
- What performance concerns exist?
- What edge cases need handling?

## Output Format

Provide a detailed design document:

```
# Feature Design: [Feature Name]

## Overview
- **Problem:** [What problem does this solve?]
- **Solution:** [How does this feature solve it?]
- **Priority:** [High/Medium/Low]
- **Effort:** [Estimated hours]

## Current State
- **Related Features:** [List existing features]
- **Dependencies:** [What must exist first?]
- **Constraints:** [What limits this design?]

## Architecture

### New Services
- [Service name]: [Purpose and responsibilities]

### Modified Services
- [Service name]: [What changes?]

### New Configs
- [Config name]: [What data?]

### Modified Configs
- [Config name]: [What changes?]

## Implementation Plan

### Phase 1: [Step Name]
- Files: [list files]
- Changes: [describe changes]
- Effort: [hours]

### Phase 2: [Step Name]
- Files: [list files]
- Changes: [describe changes]
- Effort: [hours]

## Affected Files

### New Files
- `src/server/services/NewService.lua`
- `src/shared/configs/NewConfig.lua`

### Modified Files
- `src/server/Main.server.lua` - Add service initialization
- `src/server/services/ExistingService.lua` - Add integration

## Success Criteria

Feature is complete when:
- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

## Testing Strategy

### Demo Test
1. [Step 1]
2. [Step 2]
3. [Verify result]

### Logs to Check
- `[ServiceName]` logs in Output
- `[Config]` values in state

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| [Risk] | [Impact] | [How to prevent] |

## Code Examples

### Service Pattern
\`\`\`lua
local MyService = {}

function MyService:Init()
    -- Initialize
end

function MyService:DoSomething()
    -- Implementation
end

return MyService
\`\`\`

### Config Pattern
\`\`\`lua
return {
    Property1 = value,
    Property2 = value,
}
\`\`\`

## Questions for Clarification
- [Question 1]
- [Question 2]
```

## Success Criteria

Design is complete when:
- ✅ Problem and solution are clear
- ✅ Architecture is defined
- ✅ All affected files are listed
- ✅ Implementation steps are detailed
- ✅ Success criteria are measurable
- ✅ Risks are identified
- ✅ Testing strategy is clear
- ✅ Code examples follow patterns
