from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from bot.connectors.telegram.handlers.menu.start_menu import MenuSG, get_user_info
from bot.core.statistics.proxy.proxy_users_db import usersDB
from bot.core.utils.types.userinfo import UserInfo


async def menu_settings(message: types.Message, state: FSMContext):
    await state.set_state(MenuSG.start.state)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Уведомление о заменах'))
    keyboard.add(types.KeyboardButton('Уведомление о расписании'))
    keyboard.add(types.KeyboardButton('Изменить группу'))
    keyboard.add(types.KeyboardButton('Назад'))
    await message.answer(
        'Настройки',
        reply_markup=keyboard
    )


async def get_button_text(userInfo: UserInfo, type):
    if type == 'changes':
        if userInfo.changes_notify:
            return 'Выключить'
        return 'Включить'
    elif type == 'shedule':
        if userInfo.shedule_notify:
            return 'Выключить'
        return 'Включить'


async def notify_changes(message: types.Message, state: FSMContext):
    await state.set_state(MenuSG.settings_changes.state)
    userInfo = get_user_info(message.from_user.id)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_text = await get_button_text(userInfo, 'changes')
    keyboard.add(types.KeyboardButton(button_text))
    keyboard.add(types.KeyboardButton('Назад'))

    await message.answer(
        'Уведомление о заменах на следующий день, если они появятся на сайте',
        reply_markup=keyboard
    )


async def notify_changes_enable(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)
    userInfo.changes_notify = True
    usersDB.update_user(userInfo)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_text = await get_button_text(userInfo, 'changes')
    keyboard.add(types.KeyboardButton(button_text))
    keyboard.add(types.KeyboardButton('Назад'))

    await message.answer(
        'Настройка <b>включена</b>.\nТеперь бот будет присылать замены на следующий день',
        reply_markup=keyboard
    )


async def notify_changes_disable(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)
    userInfo.changes_notify = False
    usersDB.update_user(userInfo)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_text = await get_button_text(userInfo, 'changes')
    keyboard.add(types.KeyboardButton(button_text))
    keyboard.add(types.KeyboardButton('Назад'))

    await message.answer(
        'Настройка <b>выключена</b>.\nТеперь бот не будет присылать замены на следующий день',
        reply_markup=keyboard
    )


async def notify_shedule(message: types.Message, state: FSMContext):
    await state.set_state(MenuSG.settings_shedule.state)
    userInfo = get_user_info(message.from_user.id)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_text = await get_button_text(userInfo, 'shedule')
    keyboard.add(types.KeyboardButton(button_text))
    keyboard.add(types.KeyboardButton('Назад'))
    
    await message.answer(
        'Уведомление, со списком пар на следующий день',
        reply_markup=keyboard
    )


async def notify_shedule_enable(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)
    userInfo.shedule_notify = True
    usersDB.update_user(userInfo)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_text = await get_button_text(userInfo, 'shedule')
    keyboard.add(types.KeyboardButton(button_text))
    keyboard.add(types.KeyboardButton('Назад'))

    await message.answer(
        'Настройка <b>включена</b>.\nТеперь бот будет присылать расписание на следующий день',
        reply_markup=keyboard
    )


async def notify_shedule_disable(message: types.Message, state: FSMContext):
    userInfo = get_user_info(message.from_user.id)
    userInfo.shedule_notify = False
    usersDB.update_user(userInfo)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_text = await get_button_text(userInfo, 'shedule')
    keyboard.add(types.KeyboardButton(button_text))
    keyboard.add(types.KeyboardButton('Назад'))

    await message.answer(
        'Настройка <b>выключена</b>.\nТеперь бот не будет присылать расписание на следующий день',
        reply_markup=keyboard
    )



def register_settings_menu(dp: Dispatcher):
    dp.register_message_handler(menu_settings, Text(equals='Настройки', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(menu_settings, Text(equals='Назад', ignore_case=True), state=MenuSG.settings_changes.state)
    dp.register_message_handler(menu_settings, Text(equals='Назад', ignore_case=True), state=MenuSG.settings_shedule.state)

    dp.register_message_handler(notify_changes, Text(equals='Уведомление о заменах', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(notify_changes_enable, Text(equals='Включить', ignore_case=True), state=MenuSG.settings_changes.state)
    dp.register_message_handler(notify_changes_disable, Text(equals='Выключить', ignore_case=True), state=MenuSG.settings_changes.state)


    dp.register_message_handler(notify_shedule, Text(equals='Уведомление о расписании', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(notify_shedule_enable, Text(equals='Включить', ignore_case=True), state=MenuSG.settings_shedule.state)
    dp.register_message_handler(notify_shedule_disable, Text(equals='Выключить', ignore_case=True), state=MenuSG.settings_shedule.state)