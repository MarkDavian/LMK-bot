from dataclasses import dataclass
import pymongo
# from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from bot.core.utils.types import UserInfo, GroupShedule

class SheduleDB:
    def __init__(self) -> None:
        client = pymongo.MongoClient(
            settings.mongo_host,
            settings.mongo_port
        )

        self._database = client['main']
        self._collection = self._database['shedule']

    def get_shedule(self, userInfo: UserInfo) -> dict:
        user_group = userInfo.group
        user_place = userInfo.place

        doc = self._collection.find_one(
            {
                'user_group': user_group,
                'user_place': user_place
            }
        )

        return doc

    def save_group_shedule(self, shedule: GroupShedule, userInfo: UserInfo):
        shedule = {
            'group': 'ПИ-19.2',
            'place': 'LMK',
            'shedule': {
                'Monday': {
                    1: 'Математика',
                    2: 'География'
                },
                'Tuesday': {
                    1: 'Математика',
                    2: 'География'
                }

            }
        }
        r = self._collection.insert_one(
            shedule
        )
