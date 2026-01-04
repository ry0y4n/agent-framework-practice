import asyncio
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

import json
import tempfile
import os

async def main():
    credential = AzureCliCredential()

    async with AzureAIAgentClient(credential=credential).create_agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
    ) as agent:
        thread = agent.get_new_thread()
        result = await agent.run("Tell me a short pirate joke.", thread=thread)
        print(result.text)

        # Serialize the thread state
        serialized_thread = await thread.serialize()
        serialized_json = json.dumps(serialized_thread)
        print(json.dumps(serialized_thread, indent=2))

        # Example: save to a local file (replace with DB or blob storage in production)
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "agent_thread.json")
        with open(file_path, "w") as f:
            f.write(serialized_json)

        # Read persisted JSON
        with open(file_path, "r") as f:
            loaded_json = f.read()

        reloaded_data = json.loads(loaded_json)

        # Deserialize the thread into an AgentThread tied to the same agent type
        resumed_thread = await agent.deserialize_thread(reloaded_data)

        # Continue the conversation with resumed thread
        response = await agent.run("Now tell that joke in the voice of a pirate.", thread=resumed_thread)
        print(response.text)

if __name__ == "__main__":
    asyncio.run(main())