import asyncio
import logging
import sys
from typing import Any

from google.antigravity import Agent
from google.antigravity import LocalAgentConfig
from google.antigravity.hooks import hooks


def get_funny_name(person: str) -> str:
    if person == "Bill Gates":
        return "Control-Alt-Delete Gates"
    if person == "Steve Jobs":
        return "AppleCore"
    if person == "Sam Altman":
        return "Alt Man"
    if person == "Dennis Ritchie":
        return "I See You"
    if person == "Larry Page":
        return "BackRub"
    return "I do not Know"


async def main() -> None:
    config = LocalAgentConfig(tools=[get_funny_name])
    async with Agent(config) as root_agent:
        prompt = "What is the funny name of  Dennis Ritchie ?"
        print(f"  User: {prompt}")
        response = await root_agent.chat(prompt)
        content = await response.text()
        print(content)
        # Access token usage
        conversation = root_agent.conversation
        total_usage = conversation.total_usage
        print("\n  --- Token Usage ---")
        print(f"  Prompt tokens: {total_usage.prompt_token_count}")
        print(f"  Output tokens: {total_usage.candidates_token_count}")
        print(f"  Thinking tokens: {total_usage.thoughts_token_count}")
        print(f"  Total tokens: {total_usage.total_token_count}")


if __name__ == "__main__":
    asyncio.run(main())
