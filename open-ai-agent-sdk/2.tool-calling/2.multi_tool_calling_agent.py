# Multi tool calling agent
# A simple Calculator

import time
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool
from agents.run import RunConfig

load_dotenv()

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


@function_tool
def add(num1: int, num2: int) -> int:
    return num1 + num2


@function_tool
def sub(num1: int, num2: int) -> int:
    return num1 - num2


@function_tool
def multiply(num1: int, num2: int) -> int:
    return num1 * num2


@function_tool
def divide(num1: int, num2: int) -> float:
    if num2 == 0:
        return "Cannot divide by zero"
    return num1 / num2


@function_tool
def modulus(num1: int, num2: int) -> int:
    return num1 % num2


@function_tool
def sqr_root(num: int) -> float:
    return num ** 0.5


math_agent = Agent(
    name="Math Agent",
    instructions=(
        "You are a friendly math agent that follows the DMAS rule (Division, Multiplication, Addition, Subtraction). "
        "Your job is to understand the user's math query, identify which operation they want to perform, "
        "and then call the corresponding tool (add, sub, multiply, divide, modulus, square root). "
        "When comparing two numbers, always pass the larger number as `num1` and the smaller as `num2`, unless the order matters. "
        "Once the tool returns the answer, display it in a friendly and clear way."
    ),
    tools=[add, sub, multiply, divide, modulus, sqr_root],
    model=model,
)


def main():
    print("\nWelcome to Maths Agent!")
    print("This Agent will solve your simple maths operations")

    user_input = input("You : ")

    start_time = time.time()

    result = Runner.run_sync(
        math_agent,
        user_input,
        run_config=config
    )

    end_time = time.time()
    total_time = round(end_time - start_time, 2)

    print(f"\nMath Agent: {result.final_output}")
    print(f"\n🧠 Total time taken: {total_time} seconds\n")


if __name__ == "__main__":
    main()
