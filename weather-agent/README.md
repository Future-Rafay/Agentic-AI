# 🌤️ Weather Agent CLI

A conversational, AI-powered command-line weather assistant that combines the power of Google Gemini (Generative AI) and OpenWeatherMap to deliver real-time weather information in a friendly, human-like manner.

---

## Features

- **Conversational AI:** Interact naturally with the agent to get weather updates, forecasts, and more.
- **City Extraction:** The agent intelligently extracts city names from your queries.
- **Current Weather Data:** Fetches real-time weather using OpenWeatherMap.
- **Friendly Summaries:** Uses Google Gemini to explain weather in simple, accessible language.
- **Rich CLI Output:** Beautiful, colored terminal responses powered by [rich](https://github.com/Textualize/rich).
- **Error Handling:** Graceful handling of missing data, API errors, and invalid input.

---

## Demo

![Weather Agent CLI Demo](demo.gif) <!-- Add a demo GIF if available -->

---

## Getting Started

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/weather-agent.git
cd weather-agent
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```
Or manually:
```sh
pip install requests rich python-dotenv google-generativeai
```

### 3. Get API Keys
- **Google Gemini API:** [Get your key here](https://aistudio.google.com/app/apikey)
- **OpenWeatherMap API:** [Sign up here](https://openweathermap.org/api)

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_GEMENI_API_KEY=your-gemini-api-key
WEATHER_API_KEY=your-openweather-api-key
```

---

## Usage

Run the CLI:
```sh
python main.py
```

**Example Conversation:**
```
🌤️ Welcome to Rafay's Weather Chat Agent! Ask me anything about the weather.

You: What's the weather in Paris?
Assistant: It's 18°C and sunny in Paris. A perfect day for a walk!

You: Will it rain in New York tomorrow?
Assistant: ...

You: quit
Goodbye! Stay weather-aware!
```

---

## How It Works

1. **User Input:** You type a question or city name.
2. **Intent & City Extraction:** Gemini AI analyzes your message to extract the city and intent.
3. **Weather Fetch:** The agent queries OpenWeatherMap for real-time data.
4. **Conversational Response:** Gemini generates a friendly, easy-to-understand reply.

---

## Requirements
- Python 3.8+
- API keys for Google Gemini and OpenWeatherMap

---

## Credits
- [Google Gemini API](https://ai.google.dev/gemini-api/docs)
- [OpenWeatherMap](https://openweathermap.org/api)
- [Rich](https://github.com/Textualize/rich)
- Inspired by the open-source agentic AI community

---

## License
[MIT License](LICENSE)

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Author
**Rafay**

---

> "Bringing the weather to your terminal, one friendly chat at a time!"
