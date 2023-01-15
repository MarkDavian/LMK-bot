import datetime
import pymongo
# from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

from bot.core.utils.types.userinfo import UserInfo


class UsersDB:
    def __init__(self) -> None:
        client = pymongo.MongoClient(
            settings.mongo_host,
            settings.mongo_port
        )

        self._database = client['main']

        self._users = self._database['users']

    def create_user(self, userInfo: UserInfo):
        r = self._users.insert_one(
            **userInfo.dict()
        )


usersDB = UsersDB()