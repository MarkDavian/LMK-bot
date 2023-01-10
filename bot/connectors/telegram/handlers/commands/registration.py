from aiogram import Dispatcher, types



async def register_all(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(""),
        ]
    )