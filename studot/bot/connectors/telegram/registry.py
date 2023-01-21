import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.connectors.telegram.handlers.registration import register_all
from config import settings


bot = Bot(settings.bot_api_key, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def start_tg():
    await register_all(dp)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(start_tg())