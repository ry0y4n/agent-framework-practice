import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient, AzureAIClient
from azure.identity.aio import AzureCliCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from agent_framework.observability import create_resource, enable_instrumentation

configure_azure_monitor(
    resource=create_resource(),
    enable_live_metrics=True,
)
# Optional if ENABLE_INSTRUMENTATION is already set in env vars
# enable_instrumentation()

# Create your agent with the same OpenTelemetry agent ID as registered in Foundry
credential = AzureCliCredential()
agent = AzureAIAgentClient(credential=credential).create_agent(
    name="Joker",
    instructions="You are good at telling jokes.",
    id="sample-otel-agent-id"
)

# Use the agent as normal
async def main():
    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())