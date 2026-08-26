import random

from claude_agent_sdk import McpSdkServerConfig, create_sdk_mcp_server, tool


@tool(
        name="meaning",
        description="Use this tool whenever you're asked to say what's the meaning of some amount of lives. Pass the number of lives to the \"number\" argument. Do not add your own thoughts to the answer.",
        input_schema={"number": int}
)
async def meaning(args: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": f"{args["number"]} is the answer"
            }
        ]
    }

@tool(
        name="simulate_error",
        description="Use this tool when you're asked to simulate an agent SDK error.",
        input_schema={}
)
async def simulate_error(args: dict[str, Any]) -> dict[str, Any]:
    rand_num: int = random.randint(0, 1)
    if (rand_num == 0):
        return {
            "content": [
                {
                    "type": "text",
                    "text": "The function succeeded."
                }
            ],
            "is_error": False
        }
    else:
        return {
            "content": [
                {
                    "type": "text",
                    "text": "The function failed. is_retriable=true"
                }
            ],
            "is_error": True
        }

custom_tool_server: McpSdkServerConfig = create_sdk_mcp_server(
    name="custom_tools",
    version="1.0.0",
    tools=[meaning, simulate_error]
)
