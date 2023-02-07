import datetime
import logging

from typing import Literal

import pymongo

from config import settings

from bot.core.utils.types.userinfo import UserInfo
from bot.core.utils.types.shedule import (
    WeekShedule, 
    WeekSheduleFactory, 
    DayShedule, 
    DaySheduleFactory,
    SHEDULE_DAY
)


shedule_db_logger = logging.getLogger(__name__)
shedule_db_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/SheduleDB.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
shedule_db_logger.addHandler(handler)


class SheduleDB:
    def __init__(self) -> None:
        shedule_db_logger.info('Initiating MongoDB client')
        client = pymongo.MongoClient(
            'mongodb://localhost',
            settings.mongo_port
        )

        shedule_db_logger.info('Client connected')

        self._database = client['main']

        self._change_shedule = self._database['change_shedule']
        self._combined_shedule = self._database['combined_shedule']

        shedule_db_logger.info('Client is ready')

    def _get_shedule_collection(self, week_type: Literal[0, 1, None] = None):
        """Get shedule collection by week color

        Args:
            week_type (Literal[0, 1]): 0 -- White color, 1 -- Green color

        Returns:
            Collection: Database shedule collection
        """
        if week_type is not None:
            color = week_type
        else:
            color = self._get_week_color()

        if color == 0: # white color
            return self._database['white-shedule']
        return self._database['green-shedule']

    def _get_week_color(self) -> int:
        SHEDULE_DATE = datetime.datetime(2023, 1, 2)

        now_date = datetime.datetime.now()

        days = (now_date-SHEDULE_DATE).days
        days -= days%7

        if days%14==0:
            # print('белая')
            return 0
        else:
            # print('зеленая')
            return 1

    def get_week_shedule(self, userInfo: UserInfo) -> WeekShedule:
        shedule_db_logger.info('Getting week shedule')

        shedule_collection = self._get_shedule_collection()

        doc = shedule_collection.find_one(
            {
                'Место': userInfo.place
            }
        )
        shedule_dict = doc['Курс'][str(userInfo.course)][userInfo.group]
        weekShedule = WeekSheduleFactory(shedule_dict).get()

        return weekShedule

    def get_day_shedule(self, day: str, userInfo: UserInfo) -> DayShedule:
        shedule_db_logger.info('Getting day shedule')

        shedule_collection = self._get_shedule_collection()

        doc = shedule_collection.find_one(
            {
                'Место': userInfo.place
            }
        )
        shedule_dict = {
            day: doc[userInfo.course][userInfo.group][day]
        }
        dayShedule = DaySheduleFactory(shedule_dict).get()

        return dayShedule

    def get_change_shedule(self, date: datetime.date, userInfo: UserInfo) -> DayShedule:
        shedule_db_logger.info('Getting change shedule')

        date_str = date.strftime('%Y-%m-%d')

        doc = self._change_shedule.find_one(
            {
                "Место": userInfo.place,
                "Дата": date_str

            }
        )

        shedule = doc["Курс"][str(userInfo.course)].get(userInfo.group)
        if shedule is None:
            return None

        day = SHEDULE_DAY.WEEKDAYS[date.weekday()]
        shedule = {
            day: shedule
        }

        dayShedule = DaySheduleFactory(shedule).get()

        return dayShedule

    def get_combined_shedule(self, userInfo: UserInfo) -> DayShedule:
        shedule_db_logger.info('Getting combined shedule')

        shedule_collection = self._get_shedule_collection()
        # TODO

    def save_shedule(self, placeShedule: dict, weekType: Literal[0, 1]) -> None:
        shedule_db_logger.info('Saving group shedule')

        shedule_collection = self._get_shedule_collection(week_type=weekType)

        r = shedule_collection.insert_one(placeShedule)

    def save_change_shedule(self, change: dict, date: str):
        shedule_db_logger.info('Saving change shedule')

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


def save():
    db = SheduleDB()
    import json

    with open('data/main_shedule/white/lmk_white_shedule_parsed.json', 'r') as f:
        placeShedule = json.load(f)
    db.save_shedule(placeShedule, weekType=0)

    with open('data/main_shedule/green/lmk_green_shedule_parsed.json', 'r') as f:
        placeShedule = json.load(f)
    db.save_shedule(placeShedule, weekType=1)

    # week = db.get_week_shedule(userInfo=(UserInfo(16, 'tg', 1, 'МЧМ 22-1', 'ЛМК')))

    # print(week.dict())