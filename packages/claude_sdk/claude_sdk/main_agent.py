import os

from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions,
                              ResultMessage, query)
from claude_sdk.subagents import subagents
from dotenv import load_dotenv

load_dotenv()

async def run_coordinator():
    async for message in query(
        prompt="Read /Users/ghostakr/Repo/ClaudeAgentSandbox/data/example.txt and summarize its contents.",
        options=ClaudeAgentOptions(
            agents=subagents
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
