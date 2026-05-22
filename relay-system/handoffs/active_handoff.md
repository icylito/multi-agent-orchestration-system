# Task
Implement retry limit support in the execution controller by reading the retry limit value from the existing settings.json configuration file.

# Constraints
- Only modify files that already exist in the repository
- Do not create new configuration files or sections
- Do not redesign the execution controller architecture
- Do not add new dependencies or libraries
- Only use the existing settings.json structure and parsing mechanism
- Do not modify any existing controller logic beyond adding retry limit functionality
- Do not create new classes or methods for retry handling
- Do not change the existing API or method signatures

# Expected Output
- Execution controller reads retry limit from settings.json
- Retry limit is applied to execution attempts
- Configuration key follows existing naming conventions in settings.json
- Minimal code changes to achieve retry limit functionality
- No breaking changes to existing functionality

# Notes
- The settings.json file already exists and contains configuration parsing logic
- The execution controller already handles execution flow and errors
- Retry limit should be configurable and respect existing configuration patterns
- Implementation should be consistent with existing code style and patterns
- Do not assume the existence of any retry-related classes or methods beyond what's already in the repository