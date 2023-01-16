import datetime
import logging

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


shedule_db_logger = logging.getLogger(__name__)
shedule_db_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"DataMaster.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
shedule_db_logger.addHandler(handler)


class SheduleDB:
    def __init__(self) -> None:
        shedule_db_logger.info('Initiating MongoDB client')
        client = pymongo.MongoClient(
            settings.mongo_host,
            settings.mongo_port
        )

        shedule_db_logger.info('Client connected')

        self._database = client['main']

        self._main_shedule = self._database['shedule']
        self._change_shedule = self._database['change_shedule']
        self._combined_shedule = self._database['combined_shedule']

        shedule_db_logger.info('Client is ready')

    def get_week_shedule(self, userInfo: UserInfo) -> WeekShedule:
        shedule_db_logger.info('Getting week shedule')

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
        shedule_db_logger.info('Getting day shedule')

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
        shedule_db_logger.info('Getting change shedule')

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
        shedule_db_logger.info('Getting combined shedule')

    def save_group_shedule(self, groupShedule: GroupShedule) -> None:
        shedule_db_logger.info('Saving group shedule')

        r = self._main_shedule.insert_one(
            {
                "Место": groupShedule.place,
                "Группа": groupShedule.group,
                "Курс": groupShedule.course,
                "Расписание": groupShedule.shedule.dict()
            }
        )

    def save_change_shedule(self, change: dict):
        shedule_db_logger.info('Saving change shedule')

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
