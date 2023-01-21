# from bot.core.notifier.notifier import Notifier

from bot.connectors.telegram.registry import start_tg
# from bot.connectors.telegram.registry import bot as tg_bot

from bot.connectors.vk import *


# notifier = Notifier(tg_bot=tg_bot)


async def start_connectors():
    """Start polling bots
    """
    await start_tg()