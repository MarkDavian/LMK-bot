import datetime
import logging

from typing import Literal, Union

import pymongo
# from motor.motor_asyncio import AsyncIOMotorClient

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
shedule_db_logger.addHandler(logging.StreamHandler())


class SheduleDB:
    def __init__(self) -> None:
        shedule_db_logger.info('Initiating MongoDB client')
        client = pymongo.MongoClient(
            settings.mongo_host,
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

    def get_rings(self):
        rings = [
            'Обычные дни:',
            '8:00  - 9:30',
            '9:40  - 11:10',
            '11:40 - 13:10',
            '13:30 - 15:00',
            '15:10 - 16:40',
            '16:50 - 18:20',
            '18:30 - 20:00',

            'Среда:',
            '8:00  - 9:30',
            '9:40  - 11:10',
            '11:40 - 13:10',
            'Классный час 13:30 - 14:10',
            '14:20 – 15:50',
            '16:00 – 17:30',
            '17:40 – 19:10',
            '19:20 – 20:50'
        ]
        txt = '\n'.join(rings)
        return txt

    def get_week_color(self):
        c = self._get_week_color()
        if c == 0:
            return 'Белая'
        return 'Зеленая'

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
        shedule_dict = doc['Курс'][userInfo.course][userInfo.group]
        weekShedule = WeekSheduleFactory(shedule_dict).get()

        return weekShedule

    def get_next_week_shedule(self, userInfo: UserInfo) -> WeekShedule:
        shedule_db_logger.info('Getting week shedule')

        this_week_color = self._get_week_color()
        if this_week_color == 0:
            next_week_color = 1
        else:
            next_week_color = 0

        shedule_collection = self._get_shedule_collection(next_week_color)

        doc = shedule_collection.find_one(
            {
                'Место': userInfo.place
            }
        )
        shedule_dict = doc['Курс'][userInfo.course][userInfo.group]
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
        day_shed = doc['Курс'][userInfo.course][userInfo.group].get(day, None)
        if day_shed is None:
            day = 'Понедельник'
            day_shed = doc['Курс'][userInfo.course][userInfo.group].get(day, None)

        shedule_dict = {
            day: day_shed
        }
        dayShedule = DaySheduleFactory(shedule_dict).get()

        return dayShedule

    def get_change_shedule(self, date: datetime.date, userInfo: UserInfo) -> DayShedule:
        shedule_db_logger.info('Getting change shedule')

        f_date = date
        if date.weekday() == 5:
            # Saturday to Monday
            f_date += datetime.timedelta(days=2)
        elif date.weekday() == 6:
            # Sunday to Monday
            f_date += datetime.timedelta(days=1)

        doc = self._change_shedule.find_one(
            {
                "Место": userInfo.place,
                "Дата": f_date.strftime('%Y-%m-%d')

            }
        )
        if not doc:
            today = datetime.date.today()
            f_date = today
            doc = self._change_shedule.find_one(
            {
                "Место": userInfo.place,
                "Дата": today.strftime('%Y-%m-%d')

            }
        )
        shedule = doc["Курс"].get(userInfo.course, None)
        if shedule is None:
            return f'В заменах твоего курса ({userInfo.course}) нет'
        shedule = shedule.get(userInfo.group, None)
        if shedule is None:
            return f'В заменах твоей группы ({userInfo.group}) нет'

        day = SHEDULE_DAY.WEEKDAYS[f_date.weekday()]

        shedule = {
            day: shedule
        }

        dayShedule = DaySheduleFactory(shedule).get()

        return dayShedule

    def get_combined_shedule(self, userInfo: UserInfo) -> DayShedule:
        shedule_db_logger.info('Getting combined shedule')

        shedule_collection = self._get_shedule_collection()
        # TODO

    def save_shedule(self, placeShedule: dict, place: str, weekType: Literal[0, 1]) -> None:
        shedule_db_logger.info('Saving group shedule')

        shedule_collection = self._get_shedule_collection(week_type=weekType)

        r = shedule_collection.insert_one(
            {
                "Место": place,
                **placeShedule
            }
        )

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


sheduleDB = SheduleDB()