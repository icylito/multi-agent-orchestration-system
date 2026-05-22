# Orchestra V2 Project Status

## Current Working Flow

DirectHandoff / Manager
→ ContextLoader
→ Coder
→ Reviewer
→ Human Approval
→ PatchExecutor
→ Tester
→ TestExecutor
→ Rollback if needed
→ State tracking

## Current Best Mode

DirectHandoff is currently better than Manager for small implementation tasks.

Manager should only be used for larger planning or architecture tasks.

## Working Features

- CLI-first orchestration
- Ollama model client
- Repository context loading
- Coder execution packets
- Reviewer validation
- Human-approved patch application
- Backup creation before patching
- Rollback support
- Tester agent
- Controlled command execution
- Persistent latest run state
- Direct handoff mode

## Known Issues

- Manager can add unnecessary noise for small tasks
- Tester command generation still needs stricter formatting rules
- Patch parsing requires exact FILE block format
- No automatic retry loop yet
- No multi-step task queue yet
- No memory gatekeeper integration yet

## Next Priorities

1. Make direct handoff the default workflow
2. Improve tester command reliability
3. Add retry loop when reviewer returns NEEDS_REVISION
4. Add memory gatekeeper
5. Add task history archive
6. Add safe diff preview before patch application
