from vkbottle import Keyboard, EMPTY_KEYBOARD, Text, KeyboardButtonColor
from vkbottle.bot import Message

from bot.connectors.vk.vk_bot_config import labeler, state_dispenser

from bot.connectors.vk.menu.start_menu import MenuSG, get_user_info

from bot.core.statistics.proxy.proxy_users_db import usersDB


async def get_bool_str(b: bool) -> str:
    if b:
        return 'Вкл.'
    return 'Выкл.'


@labeler.message(text='Мой профиль', state=MenuSG.start)
async def menu_start(message: Message):
    await state_dispenser.set(message.peer_id, MenuSG.profile)

    userInfo = await get_user_info(message.from_id)

    ch_ntf = await get_bool_str(userInfo.changes_notify)
    shed_ntf = await get_bool_str(userInfo.shedule_notify)

    keyboard = (
        Keyboard()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        (
            'Группа: '+userInfo.group+'\n'
            +'Курс: '+userInfo.course+'\n'
            +'Замены: '+ch_ntf+'\n'
            +'Расписание: '+shed_ntf+'\n'
        ),
        keyboard=keyboard
    )