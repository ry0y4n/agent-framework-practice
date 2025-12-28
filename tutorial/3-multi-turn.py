import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are good at telling jokes."
        ) as agent,
    ):
        thread = agent.get_new_thread()
        result1 = await agent.run("Tell me a joke about a pirate.", thread=thread)
        print(result1.text)

        result2 = await agent.run("Now add some emojis to the joke and tell it in the voice of a pirate's parrot.", thread=thread)
        print(result2.text)
        
if __name__ == "__main__":
    asyncio.run(main())
