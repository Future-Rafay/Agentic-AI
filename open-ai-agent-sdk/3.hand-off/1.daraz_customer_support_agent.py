# Hand Off
# Simple Daraz Customer Support Agent with Hand Off

import time
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, handoff, RunContextWrapper
from agents.run import RunConfig
from rich import print


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

# -------------/\-------------#

refund_agent = Agent(
    name="Refund Agent",
    instructions="""
    You are a refund specialist. 
    Ask for the order number, reason for refund, and payment method.
    Once you have details, confirm refund eligibility.
    """,
    handoffs=[],
    model=model,
)


def on_handoff(ctx: RunContextWrapper[None]):
    print("Handoff called")


refund_agent_handoff_obj = handoff(
    agent=refund_agent,
    on_handoff=on_handoff,
    tool_name_override="custom_handoff_tool_name_of_refund_agent",
    tool_description_override="Custom description",
)

# -------------/\-------------#

cancel_agent = Agent(
    name="Cancel Agent",
    instructions="""
    You are a cancellation expert.
    Help users cancel orders. Ask for order number and reason.
    If it's too late to cancel, suggest returning it.
    """,
    handoffs=[],
    model=model,
)

# -------------/\-------------#

report_agent = Agent(
    name="Report Agent",
    instructions="""
    Help users report issues (e.g. wrong item, defective product).
    Ask for order number, issue details, and photo evidence if available.
    Provide a timeline for resolution
    """,
    handoffs=[],
    model=model,
)

# -------------/\-------------#

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are the first-line support agent.
    Understand what the user wants (refund, cancellation, or report).
    Hand off to the appropriate specialist agent.
    """,
    handoffs=[refund_agent_handoff_obj, cancel_agent, report_agent],
    model=model,
)

# -------------/\-------------#


def main():
    print("\n📦 Welcome to Daraz Customer Support!")
    print("You can request a refund, cancel an order, or report an issue.\n")

    while True:
        user_input = input("🧑 You: ")

        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print("👋 Thank you! Have a great day.")
            break

        start = time.time()

        result = Runner.run_sync(
            triage_agent,
            user_input,
            run_config=config
        )

        print("\n🤖 Agent:", result.final_output)
        print(f"⏱️ Response Time: {time.time() - start:.2f} sec\n")


if __name__ == "__main__":
    main()
