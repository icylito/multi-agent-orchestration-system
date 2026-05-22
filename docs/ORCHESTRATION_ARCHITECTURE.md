# Orchestra V2 Orchestration Architecture

## Core Principle

Orchestra V2 separates deterministic execution orchestration from AI cognitive orchestration.

This prevents the AI Manager from controlling unsafe runtime behavior directly.

## Deterministic Orchestration

Handled by Python runtime:

- `app/core/pipeline.py`
- `app/core/execution_controller.py`
- `app/core/state_manager.py`
- `app/core/execute_patch.py`
- `app/core/test_executor.py`
- `app/core/rollback.py`

Responsibilities:

- Run the workflow
- Control order of execution
- Save state
- Apply patches only after approval
- Run tests only through allowlisted commands
- Rollback failed patches
- Prevent infinite loops

## Cognitive Orchestration

Handled by AI agents:

- Manager
- Coder
- Reviewer
- Tester
- MemoryGatekeeper

Responsibilities:

- Understand tasks
- Plan changes
- Generate patches
- Review implementation
- Suggest validation tests
- Summarize useful memory

## Manager Role

The Manager is optional for small tasks because direct handoff is cleaner for precise implementation requests.

The Manager should be used for:

- Multi-step tasks
- Architecture planning
- Ambiguous user requests
- Task decomposition
- Dependency ordering
- Strategic decisions

The Manager should NOT:

- Apply patches
- Run shell commands
- Modify files directly
- Override reviewer verdicts
- Bypass approval gates

## DirectHandoff Role

DirectHandoff is a simple deterministic adapter.

It converts a precise user task into a strict handoff without model expansion.

It is best for:

- Small code edits
- Simple bug fixes
- Documentation updates
- Focused implementation tasks

## Current Preferred Flow

For small tasks:

User Task
→ DirectHandoff
→ ContextLoader
→ Coder
→ Reviewer
→ DiffPreview
→ Human Approval
→ PatchExecutor
→ Tester
→ TestExecutor
→ MemoryGatekeeper

For large tasks:

User Task
→ Manager
→ Task Plan
→ Direct/Structured Handoffs
→ Execution Pipeline

## Design Rule

The AI may propose.
The deterministic runtime decides what is allowed to execute.
