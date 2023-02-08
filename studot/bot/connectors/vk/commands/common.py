from vkbottle import BaseStateGroup, Keyboard, EMPTY_KEYBOARD, Text, KeyboardButtonColor
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import CommandRule

from bot.connectors.vk.vk_bot_config import labeler, state_dispenser

from bot.connectors.vk.menu.start_menu import MenuSG

from bot.core.statistics.proxy.proxy_users_db import usersDB

from bot.core.utils.types.userinfo import UserInfo


async def get_user_info(user_id: int) -> UserInfo:
    userInfo = await usersDB.get_user_info(user_id)

    return userInfo


class RegistrationSG(BaseStateGroup):
    start = 'start'
    groupInput = 'groupInput'
    courseInput = 'courseInput'


@labeler.message(CommandRule('начать', ['/', '!']))
async def cmd_start(message: Message):
    # Remove user state
    if peer := await state_dispenser.get(message.peer_id):
        await state_dispenser.delete(peer.peer_id)

    userInfo = await get_user_info(message.from_id)
    
    if userInfo is not None:
        return
    else:
        await message.answer(
            ("Я -- бот для расписания)\n"+
            "Укажи свою группу, например ПИ 19-2"),
            keyboard=EMPTY_KEYBOARD
        )
        await state_dispenser.set(message.peer_id, RegistrationSG.groupInput)


@labeler.message(text='<group>', state=RegistrationSG.groupInput)
async def group_input(message: Message, group: str):
    keyboard = (
        Keyboard()
        .add(Text('1'))
        .add(Text('2'))
        .row()
        .add(Text('3'))
        .add(Text('4'))
    )

    await message.answer(
        "Отлично, теперь укажи свой курс",
        keyboard=keyboard
    )
    await state_dispenser.set(message.peer_id, RegistrationSG.courseInput, group=group)


@labeler.message(text='<course>', state=RegistrationSG.courseInput)
async def course_input(message: Message, course: str):
    group = message.state_peer.payload['group'].upper()

    userInfo = UserInfo(
        userID=message.from_id,
        social='vk',
        course=course,
        group=group,
        place='ЛМК'
    )
    await usersDB.create_user(userInfo)

    keyboard = (
        Keyboard()
        .add(Text('Расписание'))
        .row()
        .add(Text('Настройки'), KeyboardButtonColor.POSITIVE)
    )
    await state_dispenser.delete(message.peer_id)
    await state_dispenser.set(message.peer_id, MenuSG.start)

    await message.answer(
        "Успешно зарегистрировал тебя!)",
        keyboard=keyboard
    )

