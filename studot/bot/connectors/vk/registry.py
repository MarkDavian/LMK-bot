import asyncio

from bot.connectors.vk.vk_bot import bot


async def __start_vk():
    await bot.run_polling()


def run_vk_bot():
    asyncio.run(__start_vk())
