import pymongo
# from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

from bot.core.utils.types.user import UserInfo
from bot.core.utils.types.shedule import GroupShedule, WeekShedule, WeekSheduleFactory


class SheduleDB:
    def __init__(self) -> None:
        client = pymongo.MongoClient(
            settings.mongo_host,
            settings.mongo_port
        )

        self._database = client['main']
        self._collection = self._database['shedule']

    def get_shedule(self, userInfo: UserInfo) -> WeekShedule:
        user_group = userInfo.group
        user_place = userInfo.place

        doc = self._collection.find_one(
            {
                'Группа': user_group,
                'Место': user_place
            }
        )
        weekShedule = WeekSheduleFactory(doc).get_week_shedule()

        return weekShedule

    def save_group_shedule(self, shedule: GroupShedule) -> None:
        r = self._collection.insert_one(
            shedule.dict()
        )
