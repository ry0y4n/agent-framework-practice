import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent_framework import ChatAgent, ai_function, ChatMessage, Role
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from typing import Annotated
from pydantic import Field

# If you don't specify the name and description parameters in the ai_function decorator, the framework will automatically use the function's name and docstring as fallbacks.
@ai_function(name="weather_tool", description="Retrieve weather information for any location")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."

@ai_function(approval_mode="always_require")
def get_weather_detail(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get detailed weather information for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C, humidity 88%."

async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are a helpful assistant",
            tools=[get_weather, get_weather_detail],
        ) as agent,
    ):
        thread = agent.get_new_thread()
        result_text = await handle_approvals("Get detailed weather for Seattle and Portland", agent, thread)
        print(result_text)

async def handle_approvals(query: str, agent, thread) -> str:
    """Handle function call approvals in a loop."""
    current_input = query

    while True:
        result = await agent.run(current_input, thread=thread)

        if not result.user_input_requests:
            print(result)
            return result.text
        
        new_inputs = []

        for user_input_needed in result.user_input_requests:
            print(f"Function: {user_input_needed.function_call.name}")
            print(f"Arguments: {user_input_needed.function_call.arguments}")

            new_inputs.append(
                ChatMessage(
                    role=Role.ASSISTANT,
                    contents=[user_input_needed]
                )
            )

            user_approval = True
            new_inputs.append(
                ChatMessage(
                    role=Role.USER,
                    contents=[user_input_needed.create_response(user_approval)]
                )
            )
        current_input = new_inputs

if __name__ == "__main__":
    asyncio.run(main())
