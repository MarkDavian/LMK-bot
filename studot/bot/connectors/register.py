import multiprocessing as mp

from bot.connectors.telegram.registry import run_tg_bot
from bot.connectors.vk.registry import run_vk_bot


def start_connectors():
    """Start polling bots
    """
    run_vk()
    run_tg()


def run_vk():
    vk_bot_proc = mp.Process(target=run_vk_bot)
    vk_bot_proc.start()


def run_tg():
    tg_bot_proc = mp.Process(target=run_tg_bot)
    tg_bot_proc.start()