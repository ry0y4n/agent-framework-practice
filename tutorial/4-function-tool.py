import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent_framework import ChatAgent, ai_function
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from typing import Annotated
from pydantic import Field

# # If you don't specify the name and description parameters in the ai_function decorator, the framework will automatically use the function's name and docstring as fallbacks.
# @ai_function(name="weather_tool", description="Retrieve weather information for any location")
# def get_weather(
#     location: Annotated[str, Field(description="The location to get the weather for.")],
# ) -> str:
#     """Get the weather for a given location."""
#     return f"The weather in {location} is cloudy with a high of 15°C."

class WeatherTools:
    def __init__(self):
        self.last_location = None
    
    def get_weather(
            self,
            location: Annotated[str, Field(description="The location to get the weather for.")],
        ) -> str:
        """Get the weather for a given location."""
        return f"The weather in {location} is cloudy with a high of 15°C."
    
    def get_weather_details(self) -> int:
        """Get the detailed weather for the last requested location."""
        if self.last_location is None:
            return "No location specified yet."
        return f"The detaield weather in {self.last_location} is cloudy with a high of 15°C, low of 7°C, and 60% humidity."

async def main():
    tools = WeatherTools()
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are a helpful assistant",
            tools=[tools.get_weather, tools.get_weather_details],
        ) as agent,
    ):
        result = await agent.run("What is the weather like in Amsterdam?")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
