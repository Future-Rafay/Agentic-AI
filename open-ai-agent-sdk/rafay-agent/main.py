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
    tracing_disabled=True
)


@function_tool
def get_rafay_info() -> dict:

    rafay_info = {
        "name": "Abdul Rafay",
        "location": "Karachi, Pakistan",
        "age": 18,
        "birthdate": "2007-04-12",
        "education": {
            "current": "Intermediate 2nd Year",
            "college": "Government National College, Karachi",
            "giaic_course": {
                "current_quarter": 2,
                "quarter_1": "TypeScript",
                "quarter_2": "Next.js and Tailwind CSS",
                "future_quarter": "Agentic AI"
            }
        },
        "tech_stack": {
            "frontend": ["Next.js 14", "TypeScript", "Tailwind CSS", "shadcn/ui", "Framer Motion"],
            "backend": ["Sanity.io", "API integration", "MySQL (beginner)"],
            "languages": ["TypeScript", "JavaScript", "Python", "HTML", "CSS"],
            "tools": ["next-intl", "Vercel"]
        },
        "branding": {
            "vividcart": {
                "colors": {
                    "primary": "#4F46E5",
                    "secondary": "#10B981",
                    "background": "#F9FAFB",
                    "text": "#1F2937"
                }
            },
            "Springz": {
                "colors": {
                    "dark_green": "#134C28",
                    "lime_green": "#9BB536",
                    "olive_green": "#669E42",
                    "white": "#FFFFFF"
                },
                "slogan": "Made with Love",
                "location": "Switzerland"
            }
        },
        "projects": [
            {
                "name": "Resume Builder",
                "type": "Hackathon project",
                "platform": "GIAiC"
            },
            {
                "name": "Snake Game",
                "description": "Emoji-based snake on grass background"
            },
            {
                "name": "Springz",
                "features": ["Product, Category, Order management", "Sanity backend"]
            },
            {
                "name": "VividCart",
                "features": ["Product Listing", "Wishlist", "Cart", "Responsive UI"]
            },
            {
                "name": "Urban Stitch",
                "type": "Clothing brand",
                "note": "Requested elegant logo"
            },
            {
                "name": "Foodeez",
                "features": [
                    "Admin panel",
                    "Menu filtering",
                    "Dynamic card rendering",
                    "Multilingual support",
                    "Image animation and smooth UX"
                ]
            }
        ],
        "events": [
            {
                "name": "UI/UX Hackathon",
                "date": "2024-12-08",
                "focus": "Figma e-commerce template replication"
            },
            {
                "name": "Advanced Next.js MCQ Exam",
                "date": "2025-01-25 to 2025-01-26",
                "details": "20 advanced MCQs from Next.js documentation"
            },
            {
                "name": "Coaching Midterms",
                "date": "2024-12-19 to 2024-12-29"
            }
        ],
        "goals": {
            "python_project": "Unit converter",
            "future_goal": "Study or job opportunity in China",
            "project_vision": "Create surprising projects to impress peers and network",
            "deployment_pref": "Avoid paid services for student projects"
        },
        "learning_style": {
            "inspiration": "Math teacher's memory technique",
            "method": "Repetition",
            "reference": "The Learning Pyramid"
        }
    }

    return rafay_info


rafay_agent = Agent(
    name='Rafay Agent',
    instructions=(
        "You are a personalized assistant dedicated to Abdul Rafay. "
        "Always respond with knowledge, context, and details relevant to Rafay’s background, goals, and preferences. "
        "Leverage known data about Rafay’s education, skills, projects, and interests. "
        "Keep responses relevant, helpful, and grounded in Rafay’s real experiences and objectives. "
        "If a question is outside Rafay’s context, politely decline or redirect with a Rafay-centered suggestion."
        "You ALWAYS have to  call function get_rafay_info to get Rafay's information.\n"
    ),
    tools=[get_rafay_info],
)


def main():

    print("Welcome to Abdul Rafay Agent!")
    print("This agent is designed to provide personalized assistance based on Rafay\n")

    user_input = input("Ask Something about Rafay : ")

    result = Runner.run_sync(
        rafay_agent,
        user_input,
        run_config=config
    )

    print("Your Input:", result.input)
    print("Agent Result:", result.final_output)


if __name__ == "__main__":
    main()
