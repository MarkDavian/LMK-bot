from bot.core.utils.db.shedule import SheduleDB

from bot.core.utils.types.user import UserInfo
from bot.core.utils.types.shedule import GroupShedule, WeekShedule, DayShedule

from bot.core.statistics.metrics.metrics import metrics


class CollectorProxy_SheduleDB:
    def __init__(self, shedDB: SheduleDB) -> None:
        self.db = shedDB

    def get_week_shedule(self, userInfo: UserInfo) -> WeekShedule:
        metrics.collect('Get week shedule', *userInfo.list())
        return self.db.get_week_shedule(userInfo)

    def save_group_shedule(self, shedule: GroupShedule) -> None:
        self.db.save_group_shedule(shedule)

    def get_day_shedule(self, day: str, userInfo: UserInfo) -> DayShedule:
        metrics.collect('Get day shedule', *userInfo.list())
        self.db.get_day_shedule(day, userInfo)

    def get_change_shedule(self, userInfo: UserInfo) -> DayShedule:
        metrics.collect('Get change shedule', *userInfo.list())
        self.db.get_change_shedule(userInfo)
    
    def get_combined_shedule(self, userInfo: UserInfo) -> DayShedule:
        metrics.collect('Get combined shedule', *userInfo.list())
        self.db.get_combined_shedule(userInfo)

    def save_change_shedule(self, change: DayShedule):
        self.db.save_change_shedule(change)


sheduleDB = CollectorProxy_SheduleDB(SheduleDB())