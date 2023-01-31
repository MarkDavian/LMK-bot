from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle.bot import Message

from bot.connectors.vk.vk_bot_config import labeler, state_dispenser

from bot.connectors.vk.menu.start_menu import MenuSG, get_user_info

from bot.core.utils.types.shedule import SHEDULE_DAY
from bot.core.statistics.proxy.proxy_users_db import usersDB
from bot.core.statistics.proxy.proxy_shedule_db import sheduleDB

from bot.core.utils.types.userinfo import UserInfo


@labeler.message(text='Настройки', state=MenuSG.start)
@labeler.message(text='Назад', state=MenuSG.settings_changes)
@labeler.message(text='Назад', state=MenuSG.settings_shedule)
@labeler.message(text='Назад', state=MenuSG.profile)
async def menu_settings(message: Message):
    await state_dispenser.set(message.peer_id, MenuSG.start)

    keyboard = (
        Keyboard()
        .add(Text('Мой профиль'), KeyboardButtonColor.SECONDARY).row()
        .add(Text('Уведомление о заменах')).row()
        .add(Text('Уведомление о расписании')).row()
        .add(Text('Изменить группу')).row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        'Настройки',
        keyboard=keyboard
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


@labeler.message(text='Уведомление о заменах', state=MenuSG.start)
async def notify_changes(message: Message):
    await state_dispenser.set(message.peer_id, MenuSG.settings_changes)
    userInfo = get_user_info(message.from_id)

    keyboard = (
        Keyboard()
        .add(Text(t:=await get_button_text(userInfo, 'changes')))
        .row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        'Уведомление о заменах на следующий день, если они появятся на сайте',
        keyboard=keyboard
    )


@labeler.message(text='включить', state=MenuSG.settings_changes)
async def notify_changes_enable(message: Message):
    userInfo = get_user_info(message.from_id)
    userInfo.changes_notify = True
    usersDB.update_user(userInfo)
    
    keyboard = (
        Keyboard()
        .add(Text(t:=await get_button_text(userInfo, 'changes')))
        .row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        'Настройка включена.\nТеперь бот будет присылать замены на следующий день',
        keyboard=keyboard
    )

@labeler.message(text='выключить', state=MenuSG.settings_changes)
async def notify_changes_disable(message: Message):
    userInfo = get_user_info(message.from_id)
    userInfo.changes_notify = False
    usersDB.update_user(userInfo)

    keyboard = (
        Keyboard()
        .add(Text(t:=await get_button_text(userInfo, 'changes')))
        .row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        'Настройка выключена.\nТеперь бот не будет присылать замены на следующий день',
        keyboard=keyboard
    )


@labeler.message(text='Уведомление о расписании', state=MenuSG.start)
async def notify_shedule(message: Message):
    await state_dispenser.set(message.peer_id, MenuSG.settings_shedule)
    userInfo = get_user_info(message.from_id)

    keyboard = (
        Keyboard()
        .add(Text(t:=await get_button_text(userInfo, 'shedule')))
        .row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        'Уведомление, со списком пар на следующий день',
        keyboard=keyboard
    )


@labeler.message(text='включить', state=MenuSG.settings_shedule)
async def notify_shedule_enable(message: Message):
    userInfo = get_user_info(message.from_id)
    userInfo.shedule_notify = True
    usersDB.update_user(userInfo)

    keyboard = (
        Keyboard()
        .add(Text(t:=await get_button_text(userInfo, 'shedule')))
        .row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        'Настройка включена.\nТеперь бот будет присылать расписание на следующий день',
        keyboard=keyboard
    )


@labeler.message(text='выключить', state=MenuSG.settings_shedule)
async def notify_shedule_disable(message: Message):
    userInfo = get_user_info(message.from_id)
    userInfo.shedule_notify = False
    usersDB.update_user(userInfo)

    keyboard = (
        Keyboard()
        .add(Text(t:=await get_button_text(userInfo, 'shedule')))
        .row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )

    await message.answer(
        'Настройка выключена.\nТеперь бот не будет присылать расписание на следующий день',
        keyboard=keyboard
    )