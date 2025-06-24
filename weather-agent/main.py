### AGENT THAT ONLY GET DATA WITH CITY NAME AND NOTIFY USER ABOUT WEATHER

# import google.generativeai as genai
# import requests
# from dotenv import load_dotenv
# import os
# from rich import print

# # Load environment variables from .env file
# load_dotenv()

# GOOGLE_GEMENI_API_KEY = os.getenv("GOOGLE_GEMENI_API_KEY")
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# # Validate API keys
# if not GOOGLE_GEMENI_API_KEY:
#     print("[bold red]Google Gemini API key is not set. Please check your .env file.[/bold red]")
#     exit(1)

# if not WEATHER_API_KEY:
#     print("[bold red]Weather API key is not set. Please check your .env file.[/bold red]")
#     exit(1)

# # System Prompt for Gemini
# SYSTEM_PROMPT = """
# You are a friendly and helpful weather assistant.
# Your job is to explain weather data in simple, human-friendly language.
# You are talking to users who may not understand weather terms.
# Always be polite and informative.
# """

# # Function to fetch weather data using OpenWeatherMap API
# def get_weather_data(location: str) -> dict:
#     if not location:
#         print("[bold red]Location is not provided.[/bold red]")
#         return None

#     url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"[bold red]Error fetching weather data: {response.status_code}[/bold red]")
#             return None
#     except requests.RequestException as e:
#         print(f"[bold red]Network error: {e}[/bold red]")
#         return None

# # Function to use Gemini API to generate friendly weather summary
# def ask_gemeni_with_data(weather_info: dict, location: str):
#     try:
#         genai.configure(api_key=GOOGLE_GEMENI_API_KEY)
#         model = genai.GenerativeModel("gemini-1.5-flash")

#         temperature = weather_info['main']['temp']
#         description = weather_info['weather'][0]['description'].capitalize()
#         humidity = weather_info['main']['humidity']
#         wind_speed = weather_info['wind']['speed']

#         prompt = f"""
# {SYSTEM_PROMPT}

# Here is the weather data for {location}:
# - Temperature: {temperature}°C
# - Condition: {description}
# - Humidity: {humidity}%
# - Wind Speed: {wind_speed} m/s

# Explain this to the user in a friendly way.
# """

#         response = model.generate_content(prompt)
#         return response.text.strip()

#     except Exception as e:
#         print(f"[bold red]Error communicating with Gemini: {e}[/bold red]")
#         return None

# # Main program logic
# def main():
#     print("[bold blue]Welcome to Rafay's Weather Agent! 🌤️[/bold blue]")
#     city = input("Please enter your city: ").strip()

#     print(f"[yellow]Fetching weather data for {city}...[/yellow]")
#     weather_info = get_weather_data(city)

#     if weather_info:
#         summary = ask_gemeni_with_data(weather_info, city)
#         if summary:
#             print(f"\n[bold green]Assistant:[/bold green] {summary}")
#         else:
#             print("[bold red]Error:[/bold red] Could not generate a response from Gemini.")
#     else:
#         print("[bold red]Failed to fetch weather data.[/bold red]")

# if __name__ == "__main__":
#     main()


### AGENT THAT IS CONVERATIONAL WITH USER


import google.generativeai as genai
import requests
from dotenv import load_dotenv
import os
from rich import print

# Load environment variables
load_dotenv()

GOOGLE_GEMENI_API_KEY = os.getenv("GOOGLE_GEMENI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not GOOGLE_GEMENI_API_KEY or not WEATHER_API_KEY:
    print("[bold red]Please set your API keys in the .env file.[/bold red]")
    exit(1)

# Setup Gemini
genai.configure(api_key=GOOGLE_GEMENI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are a smart, friendly weather assistant. 
You can extract cities from user messages, decide whether to get current weather, forecasts, or rain information.
When weather data is provided, use it to generate helpful, accurate responses.
Speak clearly and in a friendly tone.
"""

# Fetch weather data (current only for now)
def get_weather_data(city: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Use Gemini to extract city and understand intent
def handle_user_query(user_input: str):
    prompt = f"""
{SYSTEM_PROMPT}

User: "{user_input}"

1. Extract the city name mentioned.
2. Determine if the user wants current weather, forecast, rain info, or something else.
3. Respond in the format: 
City: <city>
Intent: <intent description>
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[bold red]Gemini Error:[/bold red] {e}")
        return None

# Final Gemini Response
def generate_final_response(user_question: str, weather_data: dict, city: str):
    temperature = weather_data['main']['temp']
    condition = weather_data['weather'][0]['description'].capitalize()
    humidity = weather_data['main']['humidity']
    wind = weather_data['wind']['speed']

    prompt = f"""
{SYSTEM_PROMPT}

The user asked: "{user_question}"

Here is the weather data for {city}:
- Temperature: {temperature}°C
- Condition: {condition}
- Humidity: {humidity}%
- Wind Speed: {wind} m/s

Answer the user's question clearly using this data.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# Chat Loop
def main():
    print("[bold blue]🌤️ Welcome to Rafay's Weather Chat Agent! Ask me anything about the weather.[/bold blue]")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("[bold yellow]Goodbye! Stay weather-aware![/bold yellow]")
            break

        analysis = handle_user_query(user_input)

        if not analysis or "City:" not in analysis:
            print("[bold red]❌ Could not understand your question.[/bold red]")
            continue

        # Parse city from Gemini analysis
        try:
            lines = analysis.splitlines()
            city_line = next(line for line in lines if "City:" in line)
            city = city_line.split("City:")[1].strip()

            if not city:
                print("[bold red]⚠️ No city found. Try again.[/bold red]")
                continue

            print(f"[yellow]🔍 Fetching weather for {city}...[/yellow]")
            weather = get_weather_data(city)
            if not weather:
                print("[bold red]❌ Could not fetch weather. Check city name.[/bold red]")
                continue

            answer = generate_final_response(user_input, weather, city)
            print(f"\n[bold green]Assistant:[/bold green] {answer}")

        except Exception as e:
            print(f"[bold red]Error processing input: {e}[/bold red]")


if __name__ == "__main__":
    main()

