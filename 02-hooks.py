import asyncio
from typing import Any

from google.antigravity import Agent
from google.antigravity import LocalAgentConfig
from google.antigravity import types
import sys
from google.antigravity.hooks import hooks


def amazing_divide_tool(a: int, b: int):
    return a / b

# Tool Hook
@hooks.pre_tool_call_decide
async def pre_tool(data: types.ToolCall) -> types.HookResult:
    print(f"\n  CLI Hook --> Pre-tool-call: {data.name}")
    if data.name == "amazing_divide_tool":
        a = data.args["a"]
        b = data.args["b"]
        print(f" a is {a}")
        print(f" b is {b}")
        if b == 0:
            print(" What are you doing ? ")
            sys.exit(0)
            return types.HookResult(allow=False)
    return types.HookResult(allow=True)


async def main() -> None:
    config = LocalAgentConfig(
        model="gemini-3.1-flash-lite",
        hooks=[pre_tool],
        tools=[amazing_divide_tool],
    )

    async with Agent(config) as root_agent:
        print("  --- Starting Interaction ---")
        response = await root_agent.chat(" How much is 3 divided by 0")
        result = await response.text()
        print("--- Result of Division ---")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
