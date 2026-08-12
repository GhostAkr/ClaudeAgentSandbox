import os

from claude_agent_sdk import AssistantMessage, ResultMessage, query
from dotenv import load_dotenv

load_dotenv()

async def run_coordinator():
    async for message in query(
        prompt="Tell me who you are."
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
