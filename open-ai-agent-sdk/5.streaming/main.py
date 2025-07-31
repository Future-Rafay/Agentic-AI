import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, enable_verbose_stdout_logging
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)


async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
        model=model
    )

    result = Runner.run_streamed(
        agent,
        input="What is the capital of Pakistan. tell me 5 facts about it.",
        run_config=config,
    )

    # print('Agent Response:', result.final_output)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
