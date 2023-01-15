from aiogram import Dispatcher, types
from bot.connectors.telegram.handlers.commands.common import register_common_cmd
from bot.connectors.telegram.handlers.commands.shedule import register_shedule_cmd


async def register_all(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("today", 'Расписание на сегодня'),
            types.BotCommand("tomorrow", 'Расписание на завтра'),
            types.BotCommand("changes", 'Расписание замен на завтра'),
            types.BotCommand("week", 'Расписание на неделю'),
        ]
    )
    register_common_cmd(dp)
    register_shedule_cmd(dp)