

from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio
from rich import print

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client: AsyncOpenAI = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=gemini_api_key,
)

modal: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=external_client,
)

config: RunConfig = RunConfig(
    model=modal,
    model_provider=external_client,
    tracing_disabled=True
)

spanish_agent: Agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
    model=modal,
)

french_agent: Agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
    model=modal,
)

orchestrator_agent: Agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",

        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
    model=modal,
)


async def main():
    """Run the orchestrator agent to translate a message."""

    print("[bold blue]Welcome to the translation agent! You can ask me to translate messages into Spanish or French.[/bold blue]")

    user_input = input("Enter a message to translate: ")

    result = await Runner.run(orchestrator_agent, user_input, run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
