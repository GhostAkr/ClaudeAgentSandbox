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

custom_tool_server: McpSdkServerConfig = create_sdk_mcp_server(
    name="custom_tools",
    version="1.0.0",
    tools=[meaning]
)
