from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher import FSMContext


startState = State()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await state.set_state(startState.state)
    await message.answer(
        "Я -- бот для расписания)",
        reply_markup=types.ReplyKeyboardRemove()
    )

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await state.set_state(startState.state)
    await message.answer(
        "Отменено", 
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_section(message: types.Message):
    await message.reply(
        'Это просто информативная команда)'
    )


def register_common_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
