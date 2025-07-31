from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import os

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

agent: Agent = Agent(
    name="",
    instructions="",
    model=modal,
)

result: Runner = Runner.run_sync(
    agent,
    "Hello",
    run_config=config
)


def main():
    pass


if __name__ == "__main__":
    main()
