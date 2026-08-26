async def restrict_access_to_env(input_data: object, tool_use_id, context) -> object:
    file_path: str = input_data["tool_input"].get("file_path", "")
    file_name = file_path.split("/")[-1]

    if file_name == ".env":
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny",
                "permissionDecisionReason": "Cannot modify .env files",
            }
        }

    return {}

async def say_goodbye(input_data: object, tool_use_id, context) -> object:
    return {
        "hookSpecificOutput": {
            "hookEventName": input_data["hook_event_name"],
            "additionalContext": "Say goodbye after writing the tool's result"
        }
    }
