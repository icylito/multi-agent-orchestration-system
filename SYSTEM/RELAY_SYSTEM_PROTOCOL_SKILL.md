# Relay System Protocol Skill

## Overview
The relay system is located at `./relay-system/` and provides:
- Append-only logging
- Task tracking
- Rate-limit simulation
- Emergency handoff creation
- Handoff validation
- Relay continuation
- Scenario testing
- Relay status inspection

> ⚠️ **Experimental Mode**: The relay system is currently in EXPERIMENTAL MODE. Use with caution.

## Primary Commands
### `relay` Commands
- `relay --status`: Check relay status
- `relay --start-task`: Initiate a new task
- `relay --log-action`: Log an action (append-only)
- `relay --simulate-rate`: Simulate rate limiting
- `relay --create-handoff`: Generate an emergency handoff
- `relay --validate-handoff`: Validate a handoff
- `relay --continue-relay`: Continue relay processing
- `relay --log-error`: Log an error

### `relayctl` Commands
- `relayctl status`: Get relay system status
- `relayctl active`: Show active tasks
- `relayctl latest-handoff`: Retrieve latest handoff
- `relayctl run-tests`: Execute scenario tests
- `relayctl emergency <agent> <task_id>`: Trigger emergency handoff for specific agent/task

## Notes
- Commands should be executed from the relay system directory (`cd ./relay-system/`)
- Experimental features may change without notice