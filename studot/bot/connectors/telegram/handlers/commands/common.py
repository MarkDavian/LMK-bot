from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.core.statistics.proxy.proxy_users_db import usersDB

from bot.core.utils.types.userinfo import UserInfo


async def get_user_info(user_id: int) -> UserInfo:
    userInfo = await usersDB.get_user_info(user_id)

    return userInfo


class RegistrationSG(StatesGroup):
    start = State()
    groupInput = State()
    courseInput = State()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    userInfo = await get_user_info(message.from_user.id)
    
    if userInfo is not None:
        await message.answer(
            'Ты уже зарегистрирован',
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            ("Я -- бот для расписания)\n"+
            "Укажи свою группу, например ПИ 19-2"),
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(RegistrationSG.groupInput.state)


async def group_input(message: types.Message, state: FSMContext):
    group = message.text

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('1'), types.KeyboardButton('2'))
    keyboard.row(types.KeyboardButton('3'), types.KeyboardButton('4'))

    await message.answer(
        "Отлично, теперь укажи свой курс",
        reply_markup=keyboard
    )
    await state.update_data(group=group)
    await state.set_state(RegistrationSG.courseInput.state)


async def course_input(message: types.Message, state: FSMContext):
    course = message.text
    data = await state.get_data()
    group = data['group'].capitalize()

    userInfo = UserInfo(
        userID=message.from_user.id,
        social='telegram',
        course=course,
        group=group,
        place='ЛМК'
    )
    await usersDB.create_user(userInfo)
    await message.answer(
        "Успешно зарегистрировал тебя! Теперь ты можешь воспользоваться /menu )",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.finish()


def register_common_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(group_input, state=RegistrationSG.groupInput.state)
    dp.register_message_handler(course_input, state=RegistrationSG.courseInput.state)
