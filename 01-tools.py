import asyncio
from collections import Counter

from google.antigravity import Agent
from google.antigravity import LocalAgentConfig
from google.antigravity import ToolContext
from google.antigravity.hooks import policy
import pandas as pd
import warnings
import logging

# Ignore all warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)


# 1. Define a simple tool
def get_car_sales(year: int, month: str):
    df = pd.read_csv("car-sales.csv")
    result = df.query(f"year == {year} and month == '{month}'")
    return result["sales"].iloc[0]


async def main() -> None:
    # Configure the agent with both tools.
    config = LocalAgentConfig(
        model="gemini-3.1-flash-lite",
        tools=[get_car_sales],
        system_instructions=(""" 
         You use get_car_sales tool to get sales of car for a given month and year
         """),
        policies=[policy.deny_all(), policy.allow(get_car_sales.__name__)],
    )

    async with Agent(config) as root_agent:
        print(" >>> Starting ....")
        # Test simple tool
        prompt1 = "What is the sales for April 2026"
        print(f"\n  User: {prompt1}")
        response1 = await root_agent.chat(prompt1)
        print(f"  Agent: {await response1.text()}")


if __name__ == "__main__":
    asyncio.run(main())
