from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from bot.core.statistics.proxy.proxy_users_db import usersDB

from bot.core.utils.types.userinfo import UserInfo

from bot.connectors.telegram.handlers.menu.start_menu import MenuSG


async def menu_change_group(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton('Да'))
    keyboard.add(types.KeyboardButton('Нет'))
    
    await message.answer(
        'Изменить группу?',
        reply_markup=keyboard
    )
    await state.set_state(MenuSG.changeGroup.state)


async def check_answer(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if answer.lower() != 'да':
        await message.answer('Ок. Отменил', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(MenuSG.start.state)
    else:
        await message.answer('Напиши название группы')
        await state.set_state(MenuSG.menuGroupInput.state)


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
    await state.set_state(MenuSG.menuCourseInput.state)


async def course_input(message: types.Message, state: FSMContext):
    course = message.text
    data = await state.get_data()
    group = data['group']

    userInfo = UserInfo(
        userID=message.from_user.id,
        social='telegram',
        course=course,
        group=group,
        place='ЛМК'
    )
    usersDB.update_user(userInfo)
    await message.answer(
        f"Успешно! Теперь ты из {userInfo.group} {userInfo.course} курса",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.finish()


def register_group_menu(dp: Dispatcher):
    dp.register_message_handler(menu_change_group, Text(equals='Изменить группу', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(check_answer, state=MenuSG.changeGroup.state)
    dp.register_message_handler(group_input, state=MenuSG.menuGroupInput.state)
    dp.register_message_handler(course_input, state=MenuSG.menuCourseInput.state)
