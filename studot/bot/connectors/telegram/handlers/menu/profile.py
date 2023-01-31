from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.core.statistics.proxy.proxy_users_db import usersDB

from bot.connectors.telegram.handlers.menu.start_menu import MenuSG, get_user_info


def get_bool_str(b: bool) -> str:
    if b:
        return 'Вкл.'
    return 'Выкл.'


async def menu_profile(message: types.Message, state: FSMContext):
    await state.set_state(MenuSG.profile.state)
    userInfo = get_user_info(message.from_user.id)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Назад'))

    ch_ntf = get_bool_str(userInfo.changes_notify)
    shed_ntf = get_bool_str(userInfo.shedule_notify)

    await message.answer(
        (
            'Группа: '+userInfo.group+'\n'
            +'Курс: '+userInfo.course+'\n'
            +'Замены: '+ch_ntf+'\n'
            +'Расписание: '+shed_ntf+'\n'
        ),
        reply_markup=keyboard
    )


def register_profile_menu(dp: Dispatcher):
    dp.register_message_handler(menu_profile, Text(equals='Мой профиль', ignore_case=True), state=MenuSG.start.state)
