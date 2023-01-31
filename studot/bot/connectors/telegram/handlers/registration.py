from aiogram import Dispatcher, types

from bot.connectors.telegram.handlers.commands.common import register_common_cmd
from bot.connectors.telegram.handlers.commands.shedule import register_shedule_cmd
from bot.connectors.telegram.handlers.menu.start_menu import register_start_menu
from bot.connectors.telegram.handlers.menu.shedule import register_shedule_menu
from bot.connectors.telegram.handlers.menu.change_group import register_group_menu
from bot.connectors.telegram.handlers.menu.additional import register_additional_menu
from bot.connectors.telegram.handlers.menu.settings import register_settings_menu
from bot.connectors.telegram.handlers.commands.admin import register_admin_cmd
from bot.connectors.telegram.handlers.menu.profile import register_profile_menu


async def register_all(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("menu", 'Меню'),
            types.BotCommand("brake", 'Отмена/Убрать клавиатуру')
        ]
    )
    register_common_cmd(dp)
    register_shedule_cmd(dp)
    register_start_menu(dp)
    register_additional_menu(dp)
    register_shedule_menu(dp)
    register_group_menu(dp)
    register_settings_menu(dp)
    register_admin_cmd(dp)
    register_profile_menu(dp)