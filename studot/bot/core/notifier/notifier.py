import datetime

from bot.core.utils.db.shedule import sheduleDB
from bot.core.utils.db.users import usersDB
from bot.core.utils.types.userinfo import UserInfo
from bot.core.utils.types.shedule import DayShedule


class Notifier:
    def __init__(self, tg_bot, vk_bot) -> None:
        self.tg_bot = tg_bot
        self.vk_bot = vk_bot
        self.db = sheduleDB
        self.users_db = usersDB

    def notify_changes(self):
        date = datetime.date.today()
        date = datetime.date(date.year, date.month, date.day+1)

        users = self.users_db.get_users(filter={'changes_notify': True})

        for userInfo in users:
            changes = sheduleDB.get_change_shedule(date, userInfo)
            self._notify_user(userInfo, changes)

    def _notify_user(self, userInfo: UserInfo, changes: DayShedule) -> None:
        if userInfo.social == 'telegram':
            self.tg_bot.send_message(
                userInfo.userID, 
                (
                    'Появились новые замены:/n'+
                    repr(changes)
                )
            )
        elif userInfo.social == 'vk':
            self.vk_bot.send_message(
                userInfo.userID, 
                (
                    'Появились новые замены:/n'+
                    repr(changes)
                )
            )