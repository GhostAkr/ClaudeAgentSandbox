import anthropic
import os
from dotenv import load_dotenv
from claude_api.tools import str_replace_based_edit_tool, example2_opener, handle_tool

type Message = anthropic.types.Message

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def run_file_reader_agent(task: str) -> str:
    messages: list = [
        {"role": "user", "content": task}
    ]

    print("####### File reader agent messages #######")
    print(messages)

    while True:
        response: Message = client.messages.create(
            model="claude-haiku-4-5",
            messages=messages,
            max_tokens=1000,
            tools=[str_replace_based_edit_tool, example2_opener]
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        if response.stop_reason == "tool_use":
            handle_tool(response, messages)
