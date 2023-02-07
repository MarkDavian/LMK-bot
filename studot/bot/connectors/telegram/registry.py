from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.connectors.telegram.handlers.registration import register_all
from config import settings


mongoStorage = MongoStorage(
    host=settings.telegram_mongo_host,
    port=settings.mongo_port,
    db_name='telegram_states'
)

bot = Bot(settings.bot_api_key, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=mongoStorage)


async def __start_tg():
    await register_all(dp)
    await dp.start_polling()


async def run_tg_bot():
    await __start_tg()