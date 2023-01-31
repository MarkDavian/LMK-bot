from bot.connectors.vk.vk_bot import bot


async def __start_vk():
    await bot.run_polling()


async def run_vk_bot():
    await __start_vk()
