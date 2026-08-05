import anthropic
from typing import Dict
from pathlib import Path

type Message = anthropic.types.Message
type ContentBlock = anthropic.types.ContentBlock

agent_tools: list = [
    {
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool",
        "max_characters": 1000
    },
    {
        "name": "example2_opener",
        "description": "Opens files named example2.txt. Use that whenever you need to read example2.txt. Do not use it when there is no 2 at the end after example. The toll returns the contents of the file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to be read"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "math",
        "description": "Does math calculations over 2 given numbers. Use this when you need to calculate a sum or a subtraction. Returns the result of the operation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["+", "-", "unclear"]
                },
                "lhs": {
                    "type": "number",
                    "description": "The left operand. E.g. 3 in 3 + 4 or 5 in 5 - 2."
                },
                "rhs": {
                    "type": "number",
                    "description": "The right operand. E.g. 4 in 3 + 4 or 2 in 5 - 2."
                }
            }
        }
    }
]

def _handle_edit_tool(block_input: Dict[str, object]) -> str:
    if block_input["command"] == "view":
        file_path = Path(block_input["path"])
        file_contents: str = file_path.read_text()
        return file_contents
    else:
        raise Exception

def _handle_edit_example2_tool(block_input: Dict) -> str:
    file_path = Path(block_input["path"])
    file_contents: str = file_path.read_text()
    file_contents += "\nThis is a special row added by _handle_edit_example2_tool()\n"
    return file_contents

def _handle_math_tool(block_input: Dict) -> int:
    print("Using the math tool")
    lhs: int = block_input["lhs"]
    rhs: int = block_input["rhs"]

    if (block_input["operation"] == "+"):
        return lhs + rhs
    elif (block_input["operation"] == "-"):
        return lhs - rhs
    else:
        raise Exception


def handle_tool(response: Message, messages: list) -> None:
    # Put the original message from the API first
    messages.append({
        "role": "assistant",
        "content": response.content
    })

    # Go through all blocks to locate tool_use requests
    for block in response.content:
        if block.type == "tool_use":
            if block.name == "str_replace_based_edit_tool":
                result: str = _handle_edit_tool(block.input)

            elif block.name == "example2_opener":
                result: str = _handle_edit_example2_tool(block.input)

            elif block.name == "math":
                result: str = str(_handle_math_tool(block.input))

            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    }
                ]
            })
