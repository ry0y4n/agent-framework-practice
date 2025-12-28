import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from typing import Annotated
from pydantic import Field

def get_weather(
        location: Annotated[
            str,
            Field(
                description="The location to get the weather for.",
            ),
        ]
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."

weather_agent = ChatAgent(
    chat_client=AzureAIAgentClient(async_credential=AzureCliCredential()),
    name="Weather Agent",
    description="An agent that answers questions about the weather.",
    instructions="You answer questions about the weather.",
    tools=get_weather,
)

main_agent = ChatAgent(
    chat_client=AzureAIAgentClient(async_credential=AzureCliCredential()),
    instructions="You are a helpful assistant who responds in Japanese.",
    tools=weather_agent.as_tool()
)

async def main():
    result = await main_agent.run("What is the weather like in Amsterdam?")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())