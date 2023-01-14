from bot.core.utils.db.shedule import SheduleDB

from bot.core.utils.types.user import UserInfo
from bot.core.utils.types.shedule import GroupShedule, WeekShedule

from bot.core.statistics.metrics.metrics import metrics


class CollectorProxy_SheduleDB:
    def __init__(self, shedDB: SheduleDB) -> None:
        self.db = shedDB

    def get_shedule(self, userInfo: UserInfo) -> WeekShedule:
        metrics.collect('Get shedule', userInfo.place, userInfo.group, userInfo.id, userInfo.social)
        return self.db.get_week_shedule(userInfo)

    def save_group_shedule(self, shedule: GroupShedule) -> None:
        self.db.save_group_shedule(shedule)