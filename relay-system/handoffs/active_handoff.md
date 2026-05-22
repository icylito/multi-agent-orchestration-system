# Task
Implement retry limit support in the execution controller by reading the retry limit value from the existing settings.json configuration file.

# Constraints
- Only modify files that already exist in the repository
- Do not create new configuration files or sections
- Do not redesign the existing execution controller architecture
- Do not add new dependencies or external libraries
- Only read from the existing settings.json file structure
- Do not modify any existing functionality beyond adding retry logic
- Do not create new classes or methods for retry handling
- Keep changes minimal and focused

# Expected Output
- Execution controller reads retry limit from settings.json
- Retry logic implemented using existing error handling mechanisms
- Configuration value properly validated and applied
- No breaking changes to existing API or behavior
- Minimal code changes in existing controller file

# Notes
- The settings.json file already contains configuration structure
- Execution controller must use existing error handling patterns
- Retry limit should be configurable per execution
- Implementation should follow existing code style and patterns
- No new system components or services should be created
- Focus on reading existing configuration and applying retry logic