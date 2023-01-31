from vkbottle import Bot

from config import settings

from bot.connectors.vk.vk_bot_config import labeler, state_dispenser
import bot.connectors.vk.commands.common
import bot.connectors.vk.menu.shedule
import bot.connectors.vk.menu.start_menu
import bot.connectors.vk.menu.settings
import bot.connectors.vk.menu.change_group
import bot.connectors.vk.menu.additional
import bot.connectors.vk.menu.profile


bot = Bot(token=settings.vk_bot_api_key, labeler=labeler, state_dispenser=state_dispenser)

