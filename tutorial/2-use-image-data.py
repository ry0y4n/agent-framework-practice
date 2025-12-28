import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatMessage, TextContent, UriContent, DataContent, Role

message = ChatMessage(
    role=Role.USER,
    contents=[
        TextContent(text="What do you see in this image?"),
        UriContent(
            uri="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            media_type="image/jpg",
        )
    ]
)

async def main():
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="あなたは画像の内容を説明するのが得意なアシスタントです。"
        ) as agent,
    ):
        result = await agent.run(message)
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
