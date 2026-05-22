# Task
Implement retry limit support in the execution controller by reading the retry limit value from the existing settings.json configuration file.

# Constraints
- Only modify files that already exist in the repository
- Do not create new configuration files or sections
- Do not introduce new dependencies or libraries
- Do not redesign the existing execution controller architecture
- Only add retry logic to the existing execution flow
- Do not modify any existing methods beyond adding retry support
- Do not create new classes or interfaces
- Do not change the existing API or method signatures
- Do not alter the existing error handling structure

# Expected Output
- Execution controller reads retry limit from settings.json
- Execution controller implements retry logic with the configured limit
- Retry logic applies to failed executions within the existing execution flow
- No changes to configuration schema or existing settings.json structure
- Minimal code changes focused only on retry implementation

# Notes
- The settings.json file already contains configuration structure
- The execution controller already handles execution flow
- Retry logic should be applied at the execution level
- Existing error handling should remain intact
- Configuration value should be read during controller initialization
- Retry count should be tracked per execution attempt
- If retry limit is not configured, default to 0 retries