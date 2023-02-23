import asyncio

from bot.connectors.telegram.registry import run_tg_bot
from bot.connectors.vk.registry import run_vk_bot


async def __start_connectors():
    """Start polling bots
    """
    await run_tg_bot()
    await run_vk_bot()


def start_connectors():
    loop = asyncio.get_event_loop()
    loop.create_task(run_tg_bot())
    loop.create_task(run_vk_bot())
    loop.run_forever()
