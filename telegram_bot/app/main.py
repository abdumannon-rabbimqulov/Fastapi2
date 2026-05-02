import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .db import create_pool, close_pool, init_db
from .handlers import register_handlers

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

if not BOT_TOKEN:
    raise RuntimeError('BOT_TOKEN environment variable is required')
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL environment variable is required')


async def on_startup(dp: Dispatcher):
    # create db pool and init tables
    await create_pool(DATABASE_URL)
    await init_db()


async def on_shutdown(dp: Dispatcher):
    await close_pool()


def main():
    loop = asyncio.get_event_loop()
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_handlers(dp, None)

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
