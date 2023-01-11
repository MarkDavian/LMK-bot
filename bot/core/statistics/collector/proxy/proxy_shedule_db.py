from bot.core.utils.db.shedule import SheduleDB

from bot.core.utils.types.user import UserInfo
from bot.core.utils.types.shedule import GroupShedule, WeekShedule

from bot.core.statistics.collector.collector import MetricsCollector


class CollectorProxy_SheduleDB:
    def __init__(self, shedDB: SheduleDB) -> None:
        self.metrics = MetricsCollector()
        self.db = shedDB

    def get_shedule(self, userInfo: UserInfo) -> WeekShedule:
        self.metrics.new_call('Get shedule', userInfo.group, userInfo.place)
        return self.db.get_shedule(userInfo)

    def save_group_shedule(self, shedule: GroupShedule) -> None:
        self.db.save_group_shedule(shedule)