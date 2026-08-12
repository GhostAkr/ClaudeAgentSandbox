import asyncio

from claude_sdk.main_agent import run_coordinator


def main() -> None:
    asyncio.run(run_coordinator())
