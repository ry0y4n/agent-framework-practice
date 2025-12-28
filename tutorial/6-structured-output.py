import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent_framework import ChatAgent, AgentRunResponse
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from pydantic import BaseModel

class PersonInfo(BaseModel):
    """Information about a person"""
    name: str | None = None
    age: int | None = None
    occupation: str | None = None

async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            name="HelpfulAssistant",
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are a helpful assistant that extracts person information from text."
        ) as agent,
    ):
        
        # result = await agent.run(
        #     "Please provide information about Joh Smith, who is a 35-year-old software engineer.",
        #     response_format=PersonInfo
        # )
        result = await AgentRunResponse.from_agent_response_generator(
            agent.run_stream(
                "Please provide information about Joh Smith, who is a 35-year-old software engineer.",
                response_format=PersonInfo
            ),
            output_format_type=PersonInfo
        )
        
        if result.value:
            person_info = result.value
            print(f"Name: {person_info.name}, Age: {person_info.age}, Occupation: {person_info.occupation}")
        else:
            print("No structured data found in response")

if __name__ == "__main__":
    asyncio.run(main())
