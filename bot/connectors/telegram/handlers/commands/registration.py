from aiogram import Dispatcher, types
from Server.exceptions.bot_blocked import reg_block
from Server.handlers.commands.common import register_common_cmd
from Server.handlers.commands.article import register_creating_telegraph_acc, register_article_creating, register_my_accounts
from Server.handlers.commands.article.profile.my_profile import register_my_profile



async def register_all(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("new_article", "Создать новую статью"),
            types.BotCommand("my_articles", "Список моих статей"),
            types.BotCommand("my_groups", "Список моих групп"),
            types.BotCommand("my_accounts", "Список моих аккаунтов"),
            types.BotCommand("create_account", "Создать telegraph аккаунт"), 
            types.BotCommand("profile", "Мой профиль")
        ]
    )
    reg_block(dp)
    register_common_cmd(dp)
    register_creating_telegraph_acc(dp)
    register_article_creating(dp)
    register_my_accounts(dp)
    register_my_profile(dp)