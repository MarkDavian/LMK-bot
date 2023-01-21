import datetime
from typing import Literal

from bot.core.utils.db.shedule import SheduleDB

from bot.core.utils.types.user import UserInfo
from bot.core.utils.types.shedule import GroupShedule, WeekShedule, DayShedule

from bot.core.statistics.metrics.metrics import metrics


class CollectorProxy_SheduleDB:
    def __init__(self, shedDB: SheduleDB) -> None:
        self.db = shedDB

    def get_week_shedule(self, userInfo: UserInfo) -> WeekShedule:
        metrics.collect('get_week_shedule', *userInfo.list())
        return self.db.get_week_shedule(userInfo)

    def save_shedule(self, placeShedule: dict, place: str, weekType: Literal[0, 1]) -> None:
        return self.db.save_shedule(placeShedule, place, weekType)

    def get_day_shedule(self, day: str, userInfo: UserInfo) -> DayShedule:
        metrics.collect('get_day_shedule', *userInfo.list())
        return self.db.get_day_shedule(day, userInfo)

    def get_change_shedule(self, date: datetime.date, userInfo: UserInfo) -> DayShedule:
        metrics.collect('get_change_shedule', *userInfo.list())
        return self.db.get_change_shedule(date, userInfo)
    
    def get_combined_shedule(self, userInfo: UserInfo) -> DayShedule:
        metrics.collect('get_combined_shedule', *userInfo.list())
        return self.db.get_combined_shedule(userInfo)

    def save_change_shedule(self, change: dict, date: str):
        return self.db.save_change_shedule(change, date)


sheduleDB = CollectorProxy_SheduleDB(SheduleDB())