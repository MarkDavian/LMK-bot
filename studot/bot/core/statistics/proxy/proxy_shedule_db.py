import datetime
from typing import Literal

from bot.core.utils.db.shedule import SheduleDB

from bot.core.utils.types.user import UserInfo
from bot.core.utils.types.shedule import GroupShedule, WeekShedule, DayShedule

from bot.core.statistics.metrics.metrics import metrics


class CollectorProxy_SheduleDB:
    def __init__(self, shedDB: SheduleDB) -> None:
        self.db = shedDB

    async def get_week_shedule(self, userInfo: UserInfo) -> WeekShedule:
        await metrics.collect('get_week_shedule', *userInfo.list())
        return await self.db.get_week_shedule(userInfo)

    async def get_next_week_shedule(self, userInfo: UserInfo) -> WeekShedule:
        await metrics.collect('get_week_shedule', *userInfo.list())
        return await self.db.get_next_week_shedule(userInfo)

    async def save_shedule(self, placeShedule: dict, place: str, weekType: Literal[0, 1]) -> None:
        return await self.db.save_shedule(placeShedule, place, weekType)

    async def get_day_shedule(self, day: str, userInfo: UserInfo) -> DayShedule:
        await metrics.collect('get_day_shedule', *userInfo.list())
        return await self.db.get_day_shedule(day, userInfo)

    async def get_change_shedule(self, date: datetime.date, userInfo: UserInfo) -> DayShedule:
        await metrics.collect('get_change_shedule', *userInfo.list())
        return await self.db.get_change_shedule(date, userInfo)
    
    async def get_combined_shedule(self, userInfo: UserInfo) -> DayShedule:
        await metrics.collect('get_combined_shedule', *userInfo.list())
        return await self.db.get_combined_shedule(userInfo)
    
    async def get_rings(self, userInfo: UserInfo):
        await metrics.collect('get_rings', *userInfo.list())
        return await self.db.get_rings()

    async def get_week_color(self, userInfo: UserInfo) -> str:
        await metrics.collect('get_week_color', *userInfo.list())
        return await self.db.get_week_color()

    async def save_change_shedule(self, change: dict, date: str):
        return await self.db.save_change_shedule(change, date)


sheduleDB = CollectorProxy_SheduleDB(SheduleDB())