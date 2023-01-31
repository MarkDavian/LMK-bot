from typing import Optional
import logging
import datetime
from time import sleep

import telebot
import vkbottle

from config import settings

from bot.core.utils.db.shedule import sheduleDB
from bot.core.utils.db.users import usersDB
from bot.core.statistics.metrics.metrics import metrics
from bot.core.utils.types.userinfo import UserInfo
from bot.core.utils.types.shedule import DayShedule, SHEDULE_DAY


notifier_logger = logging.getLogger(__name__)
notifier_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/Notifier.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
notifier_logger.addHandler(handler)
notifier_logger.addHandler(logging.StreamHandler())


class Notifier:
    def __init__(self) -> None:
        notifier_logger.info('Notifier INIT')
        self.tg_bot = telebot.TeleBot(settings.bot_api_key)
        self.vk_bot = vkbottle.Bot(settings.vk_bot_api_key)
        self.db = sheduleDB
        self.users_db = usersDB
        notifier_logger.info('Notifier is ready')

    def alert_admin(self, error):
        self.tg_bot.send_message(settings.admin_id, error)

    def alert_admin_file(self, filename: str):
        file = open(filename, 'rb')
        self.tg_bot.send_document(settings.admin_id, file)
        file.close()

    def notify_changes(self, date: Optional[datetime.date] = None):
        notifier_logger.info('Start to notify changes')

        if date is None:
            date = datetime.date.today()
            date += datetime.timedelta(days=1)

        date_str = date.strftime('%Y-%m-%d')

        users = self.users_db.get_users(filter={'changes_notify': True})

        metrics.gauge('users_with_changes_notify', len(users))

        for userInfo in users:
            changes = sheduleDB.get_change_shedule(date, userInfo)
            self._notify_user_changes(userInfo, changes, f'Появились новые замены ({date_str}):\n')

        notifier_logger.info('Notifing is done')

    def notify_shedule(self, date: Optional[datetime.date] = None):
        notifier_logger.info('Start notifing shedule')

        if date is None:
            date = datetime.date.today()
            date += datetime.timedelta(days=1)

        day = SHEDULE_DAY.WEEKDAYS[date.weekday()]

        users = self.users_db.get_users(filter={'shedule_notify': True})

        metrics.gauge('users_with_shedule_notify', len(users))

        for userInfo in users:
            shedule = sheduleDB.get_day_shedule(day, userInfo)
            self._notify_user_changes(userInfo, shedule, f'Расписание на {day}:\n')

        notifier_logger.info('Notifing is done')

    def _notify_user_changes(self, userInfo: UserInfo, shedule: DayShedule, text: str) -> None:
        if userInfo.social == 'telegram':
            self.tg_bot.send_message(
                userInfo.userID, 
                (
                    text
                    +repr(shedule)
                )
            )
        elif userInfo.social == 'vk':
            import asyncio
            asyncio.run(
                self.vk_bot.api.messages.send(
                    user_id=userInfo.userID, 
                    message=(
                        text
                        +repr(shedule)
                    ),
                    random_id=0
                )
            )

    def start(self):
        while True:
            date = datetime.datetime.now()
            if date.weekday() != 5:
                if date.strftime("%H:%M") == '18:30':
                    self.notify_shedule()
            sleep(60)


notifier = Notifier()

def start_notifier():
    notifier_b = Notifier()
    notifier_b.start()