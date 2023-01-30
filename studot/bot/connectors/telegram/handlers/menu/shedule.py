from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from bot.core.statistics.proxy.proxy_shedule_db import sheduleDB

from bot.connectors.telegram.handlers.menu.start_menu import MenuSG, get_user_info

from bot.connectors.telegram.handlers.commands.shedule import cmd_get_shedule_today, cmd_get_shedule_tomorrow, cmd_get_change_shedule


async def menu_shedule_menu(message: types.Message, state: FSMContext):
    await state.set_state(MenuSG.start.state)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('Сегодня'), 
        types.KeyboardButton('Замены'), 
        types.KeyboardButton('Завтра'))
    keyboard.row(
        types.KeyboardButton('Эта неделя'),
        types.KeyboardButton('След. Неделя'))
    keyboard.add(types.KeyboardButton('Дополнительно'))
    keyboard.add(types.KeyboardButton('Назад'))

    await message.answer(
        'Меню расписаний',
        reply_markup=keyboard
    )


async def menu_get_today_shedule(message: types.Message, state: FSMContext):
    await cmd_get_shedule_today(message, state)


async def menu_get_tomorrow_shedule(message: types.Message, state: FSMContext):
    await cmd_get_shedule_tomorrow(message, state)


async def menu_get_change_shedule(message: types.Message, state: FSMContext):
    await cmd_get_change_shedule(message, state)


async def menu_get_this_week(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)
    shedule = sheduleDB.get_week_shedule(userInfo)

    await message.answer(
        repr(shedule)
    )


async def menu_get_next_week(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)
    shedule = sheduleDB.get_next_week_shedule(userInfo)
    
    await message.answer(
        repr(shedule)
    )


async def menu_week_color(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)
    color = sheduleDB.get_week_color(userInfo)

    await message.answer(color)


async def menu_day_shedule(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Понедельник'))
    keyboard.add(types.KeyboardButton('Вторник'))
    keyboard.add(types.KeyboardButton('Среда'))
    keyboard.add(types.KeyboardButton('Четверг'))
    keyboard.add(types.KeyboardButton('Пятница'))
    keyboard.add(types.KeyboardButton('Суббота'))
    keyboard.add(types.KeyboardButton('Назад'))
    await message.answer(
        'Какой день?',
        reply_markup=keyboard
    )
    await state.set_state(MenuSG.menuDayShedule.state)



async def day_shedule(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)
    day = message.text
    shedule = sheduleDB.get_day_shedule(day, userInfo)

    await message.answer(
        (
            f'Расписание на {shedule.name}\n'+
            repr(shedule)
        )
    )


async def rings_shedule(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)

    rings = sheduleDB.get_rings(userInfo)

    await message.answer(
        (
            f'Расписание звонков:\n'+
            rings
        )
    )


def register_shedule_menu(dp: Dispatcher):
    dp.register_message_handler(menu_shedule_menu, Text(equals='Расписание', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(menu_get_today_shedule, Text(equals='Сегодня', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(menu_get_tomorrow_shedule, Text(equals='Завтра', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(menu_get_change_shedule, Text(equals='Замены', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(menu_get_this_week, Text(equals='Эта неделя', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(menu_get_next_week, Text(equals='След. Неделя', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(menu_week_color, Text(equals='Цвет недели', ignore_case=True), state=MenuSG.additional.state)
    dp.register_message_handler(menu_day_shedule, Text(equals='Расписание на день', ignore_case=True), state=MenuSG.additional.state)
    dp.register_message_handler(rings_shedule, Text(equals='Расписание звонков', ignore_case=True), state=MenuSG.additional.state)
    dp.register_message_handler(day_shedule, state=MenuSG.menuDayShedule.state)
    dp.register_message_handler(menu_shedule_menu, Text(equals='Назад', ignore_case=True), state=MenuSG.additional.state)