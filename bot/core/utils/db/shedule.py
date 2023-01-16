import datetime
import pymongo
# from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

from bot.core.utils.types.userinfo import UserInfo
from bot.core.utils.types.shedule import (
    GroupShedule, 
    WeekShedule, 
    WeekSheduleFactory, 
    DayShedule, 
    DaySheduleFactory,
    SHEDULE_DAY
)


class SheduleDB:
    def __init__(self) -> None:
        client = pymongo.MongoClient(
            settings.mongo_host,
            settings.mongo_port
        )

        self._database = client['main']

        self._main_shedule = self._database['shedule']
        self._change_shedule = self._database['change_shedule']
        self._combined_shedule = self._database['combined_shedule']

    def get_week_shedule(self, userInfo: UserInfo) -> WeekShedule:
        doc = self._main_shedule.find_one(
            {
                'Место': userInfo.place,
                'Группа': userInfo.group
            }
        )
        shedule_dict = doc['Расписание']
        weekShedule = WeekSheduleFactory(shedule_dict).get()

        return weekShedule

    def get_day_shedule(self, day: str, userInfo: UserInfo) -> DayShedule:
        doc = self._main_shedule.find_one(
            {
                'Место': userInfo.place,
                'Группа': userInfo.group,
            }
        )
        shedule_dict = {
            day: doc['Расписание'][day]
        }
        dayShedule = DaySheduleFactory(shedule_dict).get()

        return dayShedule

    # TODO Changing places
    def get_change_shedule(self, userInfo: UserInfo) -> DayShedule:
        date = datetime.date.today()
        date = datetime.date(date.year, date.month, date.day+1)
        date_str = date.strftime('%Y-%m-%d')

        doc = self._change_shedule.find_one(
            {
                "Дата": date_str

            }
        )

        shedule = doc["Курс"][str(userInfo.course)].get(userInfo.group)
        if shedule is None:
            return None

        day = SHEDULE_DAY.WEEKDAYS[date.weekday()+1]
        shedule = {
            day: shedule
        }

        dayShedule = DaySheduleFactory(shedule).get()

        return dayShedule

    def get_combined_shedule(self, userInfo: UserInfo) -> DayShedule:
        ...

    def save_group_shedule(self, groupShedule: GroupShedule) -> None:
        r = self._main_shedule.insert_one(
            {
                "Место": groupShedule.place,
                "Группа": groupShedule.group,
                "Курс": groupShedule.course,
                "Расписание": groupShedule.shedule.dict()
            }
        )

    def save_change_shedule(self, change: dict):
        date = datetime.date.today()
        date = datetime.date(date.year, date.month, date.day+1)
        date = date.strftime('%Y-%m-%d')

        r = self._change_shedule.find_one(
            {
                "Место": "ЛМК",
                "Дата": date,
            }
        )
        if r is not None:
            re = self._change_shedule.delete_one(
                {
                    "_id": r['_id']
                }
            )
        
        r = self._change_shedule.insert_one(
            {
                "Место": "ЛМК",
                "Дата": date,
                **change
            }
        )
