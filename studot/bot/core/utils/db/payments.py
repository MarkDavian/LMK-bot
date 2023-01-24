import datetime
import logging

from typing import Literal, Union

import pymongo

from config import settings

from bot.core.utils.types.userinfo import UserInfo


payments_logger = logging.getLogger(__name__)
payments_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/PaymentsDB.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
payments_logger.addHandler(handler)
payments_logger.addHandler(logging.StreamHandler())


class PaymentsDB:
    def __init__(self) -> None:
        payments_logger.info('Initiating Payments MongoDB client')
        client = pymongo.MongoClient(
            settings.mongo_host,
            settings.mongo_port
        )

        payments_logger.info('Client connected')

        self._database = client['main']

        self._payments_collection = self._database['payments']

        payments_logger.info('Payments Client is ready')

    def get_user_subcribe(self, user_id: int = None, userInfo: UserInfo = None):
        payments_logger.info('Getting user subcribe')

        if userInfo is not None:
            user_id = userInfo.userID

        doc = self._payments_collection.find_one(
            {
                'userID': user_id
            }
        )

    def save_shedule(self, placeShedule: dict, place: str, weekType: Literal[0, 1]) -> None:
        payments_logger.info('Saving group shedule')

        shedule_collection = self._get_shedule_collection(week_type=weekType)

        r = shedule_collection.insert_one(
            {
                "Место": place,
                **placeShedule
            }
        )

    def save_change_shedule(self, change: dict, date: str):
        payments_logger.info('Saving change shedule')

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


paymentsDB = PaymentsDB()