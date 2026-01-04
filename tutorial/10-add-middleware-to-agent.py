import asyncio
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import FunctionInvocationContext
from typing import Callable, Awaitable

# async def logging_agent_middleware(
#     context: AgentRunContext,
#     next: Callable[[AgentRunContext], Awaitable[None]],
# ) -> None:
#     """Simple middleware that logs agent execution."""
#     print("Agent starting...")

#     # Continue to agent execution
#     await next(context)

#     print("Agent finished!")

def get_time():
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

async def logging_function_middleware(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Awaitable[None]],
) -> None:
    """Middleware that logs function calls."""
    print(f"Calling function: {context.function.name}")

    await next(context)

    print(f"Function result: {context.result}")

async def main():
    credential = AzureCliCredential()

    async with AzureAIAgentClient(credential=credential).create_agent(
        name="GreetingAgent",
        instructions="You can tell the current time.",
        tools=get_time,
        middleware=logging_function_middleware
    ) as agent:
        result = await agent.run("What time is it?")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())