from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.core.statistics.proxy.proxy_users_db import usersDB

from bot.core.utils.types.userinfo import UserInfo
from bot.core.utils.types.user import User


class RegistrationSG(StatesGroup):
    start = State()
    groupInput = State()
    courseInput = State()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        ("Я -- бот для расписания)\n"+
        "Укажи свою группу, например ПИ 19-2"),
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationSG.groupInput.state)


async def group_input(message: types.Message, state: FSMContext):
    group = message.text
    await message.answer(
        "Отлично, теперь укажи свой курс цифрой (1-4)"
    )
    await state.update_data(group=group)
    await state.set_state(RegistrationSG.courseInput.state)


async def course_input(message: types.Message, state: FSMContext):
    course = message.text
    group = await state.get_data('group')

    userInfo = UserInfo(
        id=message.from_user.id,
        social='telegram',
        course=course,
        group=group,
        place='ЛМК'
    )
    usersDB.create_user(userInfo)
    await message.answer(
        "Успешно зарегистрировал тебя! Теперь ты можешь воспользоваться командами)"
    )

    await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Отменено", 
        reply_markup=types.ReplyKeyboardRemove()
    )


def register_common_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(group_input, state=RegistrationSG.groupInput.state)
    dp.register_message_handler(course_input, state=RegistrationSG.courseInput.state)
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
