from vkbottle import Keyboard, Text, KeyboardButtonColor, EMPTY_KEYBOARD
from vkbottle.bot import Message

from bot.connectors.vk.vk_bot_config import labeler, state_dispenser

from bot.connectors.vk.menu.start_menu import MenuSG, get_user_info

from bot.core.statistics.proxy.proxy_users_db import usersDB

from bot.core.utils.types.userinfo import UserInfo


@labeler.message(text='Изменить группу', state=MenuSG.start)
async def menu_change_group(message: Message):
    await state_dispenser.set(message.peer_id, MenuSG.changeGroup)
    keyboard = (
        Keyboard()
        .add(Text('Да'), KeyboardButtonColor.NEGATIVE)
        .row()
        .add(Text('Нет'), KeyboardButtonColor.POSITIVE)
    )
    
    await message.answer(
        'Изменить группу?',
        keyboard=keyboard
    )


@labeler.message(text='<answer>', state=MenuSG.changeGroup)
async def check_answer(message: Message, answer: str):
    if answer.lower() != 'да':
        keyboard = (
            Keyboard()
            .add(Text('Расписание'))
            .row()
            .add(Text('Настройки'), KeyboardButtonColor.POSITIVE)
        )
        await message.answer('Ок. Отменил', keyboard=keyboard)
        await state_dispenser.set(message.peer_id, MenuSG.start)
    else:
        await message.answer('Напиши название группы', keyboard=EMPTY_KEYBOARD)
        await state_dispenser.set(message.peer_id, MenuSG.menuGroupInput)


@labeler.message(text='<group>', state=MenuSG.menuGroupInput)
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
    await state_dispenser.set(message.peer_id, MenuSG.menuCourseInput, group=group)


@labeler.message(text='<course>', state=MenuSG.menuCourseInput)
async def course_input(message: Message, course: str):
    group = message.state_peer.payload['group'].capitalize()

    userInfo = await get_user_info(message.from_id)
    userInfo.course = course
    userInfo.group = group

    keyboard = (
        Keyboard()
        .add(Text('Мой профиль')).row()
        .add(Text('Уведомление о заменах')).row()
        .add(Text('Уведомление о расписании')).row()
        .add(Text('Изменить группу')).row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await usersDB.update_user(userInfo)
    await message.answer(
        f"Успешно! Теперь ты из {userInfo.group}, {userInfo.course} курса",
        keyboard=keyboard
    )
    await state_dispenser.set(message.peer_id, MenuSG.start)
