from aiogram.types import ContentType, ParseMode
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, SwitchTo, Column
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.media import StaticMedia


class UserMenuSG(StatesGroup):
    start = State()

    achieve_start = State()
    achieve_see = State()
    achieve_unlocked_boars = State()
