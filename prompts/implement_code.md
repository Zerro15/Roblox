# Implement Code Prompt

## Task
Implement a game feature based on an approved design plan.

## Instructions

### 1. Read the Design Plan
- Understand the feature requirements
- Review affected files list
- Note implementation steps
- Identify success criteria

### 2. Explore Existing Code
- Read all affected files
- Understand existing patterns
- Identify where changes go
- Note any dependencies

### 3. Implement Step by Step
For each implementation phase:
1. Read the file to be modified
2. Identify the exact location for changes
3. Make minimal, focused edits
4. Preserve existing code style
5. Add necessary imports at top of file

### 4. Follow Code Patterns

**Service Pattern:**
```lua
local MyService = {}

function MyService:Init()
    -- Initialize service
end

function MyService:PublicMethod()
    -- Public API
end

local function _PrivateHelper()
    -- Private helper
end

return MyService
```

**Config Pattern:**
```lua
return {
    PropertyName = {
        subproperty = value,
    },
}
```

**Bootstrap Pattern:**
```lua
local Service = require(path.to.Service)
Service:Init()
```

### 5. Add Imports Correctly
- All imports at top of file
- Use relative paths from `ReplicatedStorage`
- Follow existing import style

### 6. Test Each Change
After each file edit:
1. Run `.\scripts\build_place.ps1`
2. Verify build succeeds
3. Check for Lua syntax errors
4. Note any warnings

### 7. Create PR
When all changes are complete:
1. Verify working tree is clean
2. Create feature branch: `git checkout -b feature/name`
3. Stage changes: `git add src/`
4. Commit with clear message: `git commit -m "Add feature description"`
5. Push branch: `git push origin feature/name`
6. Create PR: `gh pr create --title "..." --body "..."`

## Output Format

Provide implementation summary:

```
# Implementation: [Feature Name]

## Changes Made

### New Files
- `src/server/services/NewService.lua` - [Purpose]
- `src/shared/configs/NewConfig.lua` - [Purpose]

### Modified Files
- `src/server/Main.server.lua` - Added service initialization
- `src/server/services/ExistingService.lua` - Added integration

## Build Verification
- ✅ Build succeeds: `.\scripts\build_place.ps1`
- ✅ No Lua syntax errors
- ✅ All imports correct
- ✅ Code follows patterns

## PR Details
- **Branch:** feature/tower-spending
- **Commits:** [List commits]
- **PR Number:** [If created]

## Next Steps
- Testing via `team_review_demo.ps1`
- Review and approval
- Safe merge via `pr_safe_merge.ps1`
```

## Code Style Guidelines

### Naming Conventions
- **Services:** PascalCase (MyService)
- **Functions:** camelCase (myFunction)
- **Constants:** UPPER_SNAKE_CASE (MY_CONSTANT)
- **Local variables:** camelCase (myVariable)

### Formatting
- **Indentation:** 4 spaces (or 1 tab)
- **Line length:** Keep reasonable (80-120 chars)
- **Comments:** Explain "why", not "what"
- **Blank lines:** Between logical sections

### Documentation
```lua
-- Brief description of what this does
-- @param paramName (type) - description
-- @return (type) - description
function MyService:MyFunction(paramName)
    -- Implementation
end
```

## Common Patterns

### Service Initialization
```lua
-- In Main.server.lua
local MyService = require(ReplicatedStorage.Shared.services.MyService)
MyService:Init()
```

### Config Usage
```lua
local MyConfig = require(ReplicatedStorage.Shared.configs.MyConfig)
local value = MyConfig.PropertyName.subproperty
```

### Event Handling
```lua
local signal = Instance.new("BindableEvent")
signal:Fire(data)
signal.Event:Connect(function(data)
    -- Handle event
end)
```

### Service Dependencies
```lua
local MyService = {}
local OtherService = require(ReplicatedStorage.Shared.services.OtherService)

function MyService:Init()
    OtherService:DoSomething()
end
```

## Verification Checklist

Before creating PR:
- ✅ All files read and understood
- ✅ All changes implemented
- ✅ Build succeeds
- ✅ No syntax errors
- ✅ Imports are correct
- ✅ Code follows patterns
- ✅ Comments are clear
- ✅ Working tree is clean
- ✅ Feature branch created
- ✅ Changes committed
- ✅ Branch pushed

## Troubleshooting

### Build Fails
1. Check error message
2. Verify Lua syntax
3. Check imports
4. Verify file paths
5. Run `rojo build` directly

### Syntax Error
1. Check line number in error
2. Verify brackets and parentheses
3. Check string quotes
4. Verify function definitions

### Import Error
1. Verify file path is correct
2. Check file exists
3. Verify relative path from ReplicatedStorage
4. Check file name spelling

## Success Criteria

Implementation is complete when:
- ✅ All design requirements are met
- ✅ Code follows project patterns
- ✅ Build succeeds
- ✅ PR is created
- ✅ Ready for testing
