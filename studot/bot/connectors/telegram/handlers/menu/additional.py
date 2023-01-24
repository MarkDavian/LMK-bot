from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from bot.connectors.telegram.handlers.menu.start_menu import MenuSG


async def menu_additional(message: types.Message, state: FSMContext):
    await state.set_state(MenuSG.additional.state)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Расписание на день'))
    keyboard.add(types.KeyboardButton('Расписание звонков'))
    keyboard.add(types.KeyboardButton('Цвет недели'))
    keyboard.add(types.KeyboardButton('Назад'))
    await message.answer(
        'Дополнительно',
        reply_markup=keyboard
    )



def register_additional_menu(dp: Dispatcher):
    dp.register_message_handler(menu_additional, Text(equals='Дополнительно', ignore_case=True), state=MenuSG.start.state)
    dp.register_message_handler(menu_additional, Text(equals='Назад', ignore_case=True), state=MenuSG.menuDayShedule.state)
