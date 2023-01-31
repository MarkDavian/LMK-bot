from vkbottle import BaseStateGroup, Keyboard, EMPTY_KEYBOARD, Text, KeyboardButtonColor
from vkbottle.bot import Message

from bot.connectors.vk.vk_bot_config import labeler, state_dispenser

from bot.core.statistics.proxy.proxy_users_db import usersDB

from bot.core.utils.types.userinfo import UserInfo


def get_user_info(user_id: int) -> UserInfo:
    userInfo = usersDB.get_user_info(user_id)

    return userInfo


class MenuSG(BaseStateGroup):
    start = 'start'

    menuGroupInput = 'menuGroupInput'
    menuCourseInput = 'menuCourseInput'

    menuDayShedule = 'menuDayShedule'

    additional = 'additional'

    settings_changes = 'settings_changes'
    settings_shedule = 'settings_shedule'

    changeGroup = 'changeGroup'

    profile = 'profile'


@labeler.message(lev='меню')
@labeler.message(text='Меню')
@labeler.message(text='/menu')
@labeler.message(text='Назад', state=MenuSG.start)
async def menu_start(message: Message):
    keyboard = (
        Keyboard()
        .add(Text('Расписание'))
        .row()
        .add(Text('Настройки'), KeyboardButtonColor.POSITIVE)
    )
    await message.answer(
        'Меню',
        keyboard=keyboard
    )
    await state_dispenser.set(message.peer_id, MenuSG.start)


@labeler.message(text='убрать')
async def menu_brake(message: Message):
    await message.answer(
        'Отменено/Клавиатура убрана',
        keyboard=EMPTY_KEYBOARD
    )

    if peer := await state_dispenser.get(message.peer_id):
        await state_dispenser.delete(peer.peer_id)
