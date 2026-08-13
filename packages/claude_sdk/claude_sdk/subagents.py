from claude_agent_sdk import AgentDefinition


subagents = {
    "custom_reader": AgentDefinition(
        description="Reads files and summarizes its contents. You have to use it whenever you need to read any text file",
        prompt="After reading a file summarize its contents and return the summary.",
        disallowedTools=["Read"]
    )
}
