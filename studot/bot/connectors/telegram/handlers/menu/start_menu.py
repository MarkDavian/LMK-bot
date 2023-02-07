from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.core.statistics.proxy.proxy_users_db import usersDB

from bot.core.utils.types.userinfo import UserInfo


async def get_user_info(user_id: int) -> UserInfo:
    userInfo = await usersDB.get_user_info(user_id)

    return userInfo


class MenuSG(StatesGroup):
    start = State()

    menuGroupInput = State()
    menuCourseInput = State()

    menuDayShedule = State()

    additional = State()

    settings_changes = State()
    settings_shedule = State()

    changeGroup = State()

    profile = State()


async def menu_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Расписание'))
    keyboard.add(types.KeyboardButton('Настройки'))
    await message.answer(
        'Меню',
        reply_markup=keyboard
    )
    await state.set_state(MenuSG.start.state)


async def menu_brake(message: types.Message, state: FSMContext):
    await message.answer(
        'Отменено/Клавиатура убрана',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()


def register_start_menu(dp: Dispatcher):
    dp.register_message_handler(menu_start, commands="menu", state="*")
    dp.register_message_handler(menu_brake, commands="brake", state="*")
    dp.register_message_handler(menu_start, Text(equals='Назад', ignore_case=True), state=MenuSG.start.state)
