from ..common import *

profile = Window(
        Const('Профиль'),
        SwitchTo(Const('Сменить группу'), id='inline_start', state=UserMenuSG.inline_step_one),
        SwitchTo(Const('Назад'), id='back', state=UserMenuSG.start),
        state=UserMenuSG.profile_start,
        parse_mode=ParseMode.HTML
    )