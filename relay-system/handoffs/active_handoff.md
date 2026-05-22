# Task
Implement retry limit support in the execution controller by reading the retry limit value from the existing settings.json configuration file.

# Constraints
- Only modify the execution controller implementation
- Read retry limit from settings.json configuration
- Do not create new configuration files or modify existing ones beyond reading
- Do not change the existing execution controller architecture
- Do not implement new retry logic - only add configuration reading
- Do not add new dependencies or libraries
- Do not modify any other controllers or system components

# Expected Output
- Execution controller successfully reads retry limit from settings.json
- Configuration value is accessible within execution controller logic
- No existing functionality is broken
- Minimal code changes to achieve the requirement

# Notes
- The settings.json file already exists and contains retry configuration
- The execution controller should be able to access the retry limit value
- This is a configuration reading task only - no logic changes required
- Ensure the implementation follows existing code patterns and conventions