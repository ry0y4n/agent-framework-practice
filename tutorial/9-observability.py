import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from agent_framework.observability import configure_otel_providers
configure_otel_providers()

credential = AzureCliCredential()
agent = AzureAIAgentClient(credential=credential).create_agent(
    name="Joker",
    instructions="You are good at telling jokes.",
)

async def main():
    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())