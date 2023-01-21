from aiogram_dialog import Dialog
from aiogram_dialog.widgets.kbd import Column, SwitchTo

from .common import Window, StaticMedia, Const, UserMenuSG, ParseMode

from .achievements import achieveWINS


helps = Window(
        Const('Главное меню'),
        Column(
            SwitchTo(Const('Профиль'), id='profile', state=UserMenuSG.profile_start),
            SwitchTo(Const('Расписание'), id='shedule', state=UserMenuSG.shedule_start),
            SwitchTo(Const('Замены'), id='changes', state=UserMenuSG.changes_start),
            SwitchTo(Const('Знакомства'), id='love', state=UserMenuSG.love_start),
            SwitchTo(Const('Услуги'), id='funcs', state=UserMenuSG.funcs_start)
        ),
        state=UserMenuSG.start,
        parse_mode=ParseMode.HTML
    )


dialog = Dialog(
    helps,
    *achieveWINS
)
