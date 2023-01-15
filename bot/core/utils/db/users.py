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
            userInfo.dict()
        )

    def get_user_info(self, user_id: int) -> UserInfo:
        r = self._users.find_one(
            {
                'userID': user_id
            }
        )
        userInfo = UserInfo(
            userID=r['userID'],
            social=r['social'],
            course=r['course'],
            group=r['group'],
            place=r['place']
        )
        return userInfo


usersDB = UsersDB()