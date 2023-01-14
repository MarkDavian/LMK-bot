from bot.connectors.telegram.registry import start_tg
from bot.connectors.vk import *


async def start_connectors():
    """Start polling bots
    """
    await start_tg()