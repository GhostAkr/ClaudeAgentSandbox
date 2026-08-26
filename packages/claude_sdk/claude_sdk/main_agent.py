from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions,
                              HookMatcher, ResultMessage, query)
from claude_sdk.hooks import restrict_access_to_env
from claude_sdk.subagents import subagents
from dotenv import load_dotenv

load_dotenv()

files_to_read: list(str) = [
    "/Users/ghostakr/Repo/ClaudeAgentSandbox/data/example.txt",
    "/Users/ghostakr/Repo/ClaudeAgentSandbox/.env"
]

async def run_coordinator():
    async for message in query(
        prompt=f"Read {files_to_read[1]} and summarize its contents.",
        options=ClaudeAgentOptions(
            # agents=subagents,  # Uncomment if you want to test subagents. Note that it might conflict with the hooks
            hooks={
                "PreToolUse": [HookMatcher(matcher="Read|Edit", hooks=[restrict_access_to_env])]
            }
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
