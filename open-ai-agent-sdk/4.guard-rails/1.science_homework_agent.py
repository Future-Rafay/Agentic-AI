# Guardrails Example: Science Homework Agent
# This example demonstrates how to create a guardrail that prevents an agent from doing math homework.

from pydantic import BaseModel
from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio
from rich import print, prompt

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


class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=modal,
)


@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    # print(f"Guardrail agent output: {result.final_output}")
    # print(f"Guardrail agent output: {result.final_output.is_math_homework}")

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )


science_home_work_agent = Agent(
    name="Science Homework agent",
    instructions="You are a helpful assistant that can answer questions about science homework. ",
    input_guardrails=[math_guardrail],
    model=modal,
)


async def main():
    print("[bold green]Welcome to the Science Homework Agent! \nThis agent will help you with your science homework, but it will not do your math homework for you. [/bold green]\n")

    user_input = prompt.Prompt.ask(
        "[bold blue]Please enter your question: [/bold blue]")

    try:
        result = await Runner.run(science_home_work_agent, user_input, run_config=config)
        print(f"Agent : {result.final_output}")

    except InputGuardrailTripwireTriggered:
        print("Agent :[bold red]😢 It seems like you are asking for help with math homework. Please try to rephrase your question or ask about science homework instead.[/bold red]")

if __name__ == "__main__":
    asyncio.run(main())
