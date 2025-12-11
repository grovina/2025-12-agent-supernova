# Supernova

CLI chatbot agent with tools for weather, time, and asking Alexey via Telegram.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with:

   ```
   OPENAI_API_KEY=your_key_here
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

3. Run:

   ```bash
   python main.py
   ```

## Tools

- `get_weather(city)` - Get weather for a city
- `get_date_and_time()` - Get current date and time
- `ask_alexey(question)` - Ask Alexey a Python-related question via Telegram
