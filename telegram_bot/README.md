Simple Telegram bot using aiogram that collects user info and small orders and saves them to Postgres.

Setup (development with Docker Compose):

1. Copy .env.example to .env and fill BOT_TOKEN and DATABASE_URL if needed.

2. Start services:
   docker compose up --build

3. The bot will start and connect to Postgres. Use Telegram to interact with your bot.

Tables are created automatically on startup.
