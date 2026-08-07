import anthropic
import os
from dotenv import load_dotenv
from anthropiccertification.tools import agent_tools, handle_tool

type Message = anthropic.types.Message

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def run_agent_loop() -> None:
    messages: list = [
        {"role": "user", "content": "Calculate 2 + 3 and give a brief summary of the contents of /home/ghostakr/Repo/AnthropicCertification/data/example.txt"}
    ]

    while True:
        print("####### Messages #######")
        print(messages)

        response: Message = client.messages.create(
            model="claude-haiku-4-5",
            messages=messages,
            max_tokens=1000,
            tools=agent_tools
        )

        print("####### Response #######")
        print(response.content)

        if response.stop_reason == "end_turn":
            print("####### Result #######")
            print(response.content[0].text)
            break

        if response.stop_reason == "tool_use":
            handle_tool(response, messages)
