# Audit Codebase Prompt

## Task
Analyze the Roblox Tower Defense prototype codebase to understand current state, architecture, and patterns.

## Instructions

1. **Explore Directory Structure**
   - List main directories: `src/`, `tools/`, `scripts/`, `bridge/`, `docs/`
   - Identify key files and their purposes
   - Note any missing or incomplete directories

2. **Review Game Code** (`src/`)
   - List all Lua files in `src/client/`, `src/server/`, `src/shared/`
   - Identify service files in `src/server/services/`
   - Review config files in `src/shared/configs/`
   - Note code patterns and conventions

3. **Analyze Services**
   For each service in `src/server/services/`:
   - What does it do?
   - What functions does it expose?
   - What configs does it use?
   - What other services does it depend on?

4. **Review Configurations**
   For each config in `src/shared/configs/`:
   - What data does it define?
   - How is it used by services?
   - What properties are configurable?

5. **Check Bootstrap Code**
   - Read `src/server/Main.server.lua` - what initializes?
   - Read `src/client/Main.client.lua` - what initializes?
   - Identify initialization order and dependencies

6. **Review Build System**
   - Check `default.project.json` - what does Rojo map?
   - Verify `src/` structure matches Rojo config
   - Note any build-related issues

7. **Examine Tools**
   - List Python files in `tools/studio_operator/`
   - Identify main entry points
   - Note dependencies and requirements

8. **Check Documentation**
   - List existing `.md` files
   - Identify what's documented and what's missing
   - Note any outdated documentation

## Output Format

Provide a structured audit report:

```
# Codebase Audit Report

## Directory Structure
- [list main directories and purpose]

## Game Code Analysis
### Services
- [list services with brief description]

### Configs
- [list configs with brief description]

### Bootstrap
- [describe initialization flow]

## Build System
- [describe Rojo mapping]
- [note any issues]

## Tools & Automation
- [list main tools]
- [note dependencies]

## Documentation
- [list existing docs]
- [identify gaps]

## Code Patterns
- [describe Lua conventions]
- [describe service patterns]
- [describe config patterns]

## Risks & Issues
- [list any problems found]
- [note missing pieces]

## Recommendations
- [suggest improvements]
```

## Success Criteria

Audit is complete when:
- ✅ All directories explored
- ✅ All services documented
- ✅ All configs reviewed
- ✅ Bootstrap flow understood
- ✅ Build system verified
- ✅ Code patterns identified
- ✅ Risks documented
