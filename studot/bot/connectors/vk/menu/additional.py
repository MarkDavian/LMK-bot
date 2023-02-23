from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle.bot import Message

from bot.connectors.vk.vk_bot_config import labeler, state_dispenser

from bot.connectors.vk.menu.start_menu import MenuSG


@labeler.message(text='[club218297281|@studotbot] дополнительно', state=MenuSG.start)
@labeler.message(text='дополнительно', state=MenuSG.start)
@labeler.message(text='[club218297281|@studotbot]', state=MenuSG.menuDayShedule)
@labeler.message(text='назад', state=MenuSG.menuDayShedule)
async def menu_additional(message: Message):
    await state_dispenser.set(message.peer_id, MenuSG.additional)
    keyboard = (
        Keyboard()
        .add(Text('Расписание на день')).row()
        .add(Text('Расписание звонков')).row()
        .add(Text('Цвет недели')).row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        'Дополнительно',
        keyboard=keyboard
    )