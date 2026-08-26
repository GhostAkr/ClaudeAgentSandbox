from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions,
                              HookMatcher, ResultMessage, query)
from claude_sdk.hooks import restrict_access_to_env, say_goodbye
from claude_sdk.subagents import subagents
from claude_sdk.tools import custom_tool_server
from dotenv import load_dotenv

load_dotenv()

system_prompt_text: str = """
    If a tool call fails, read it's \"is_retriable\" boolean property. If it is True, repeat the call tool.
    However do not make more than 3 calls of the same tool per a session. If \"is_retriable\" is False, fail immediatly and say that to
    the user.
"""
system_prompt={
    "type": "preset",
    "preset": "claude_code",
    "append": system_prompt_text
}

files_to_read: list(str) = [
    "/Users/ghostakr/Repo/ClaudeAgentSandbox/data/example.txt",
    "/Users/ghostakr/Repo/ClaudeAgentSandbox/.env"
]
read_message: str = f"Read {files_to_read[0]} and summarize its contents."

life_message: str = "What's the meaning of 9 lives?"
error_message: str = "Simulate an agent SDK error"

async def run_coordinator():
    async for message in query(
        prompt=error_message,
        options=ClaudeAgentOptions(
            # agents=subagents,  # Uncomment if you want to test subagents. Note that it might conflict with the hooks
            system_prompt=system_prompt,
            hooks={
                "PreToolUse": [HookMatcher(matcher="Read|Edit", hooks=[restrict_access_to_env])],
                "PostToolUse": [HookMatcher(matcher="Read|Edit", hooks=[say_goodbye])]
            },
            mcp_servers={"custom_tool_server": custom_tool_server},
            allowed_tools=["mcp__custom_tool_server__meaning", "mcp__custom_tool_server__simulate_error"]
        )
    ):
        print("==================")
        print("Conversation round")
        print("==================")

        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(f"Intermediate message: {block.text}")
                elif hasattr(block, "name"):
                    print(f"Running the {block.name} tool.")
        elif isinstance(message, ResultMessage):
            print(f"Result: {message.subtype}")
