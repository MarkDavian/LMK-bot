from bot.core.utils.db.shedule import SheduleDB

from bot.core.utils.types.user import UserInfo
from bot.core.utils.types.shedule import GroupShedule, WeekShedule, WeekSheduleFactory


class CollectorProxy_SheduleDB:
    def __init__(self, shedDB: SheduleDB) -> None:
        self.db = shedDB

    def get_shedule(self, userInfo: UserInfo) -> WeekShedule:
        return self.db.get_shedule(userInfo)

    def save_group_shedule(self, shedule: GroupShedule) -> None:
        self.db.save_group_shedule(shedule)