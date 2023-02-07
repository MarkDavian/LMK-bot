import datetime
# import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

from bot.core.utils.types.userinfo import UserInfo


class UsersDB:
    def __init__(self) -> None:
        client = AsyncIOMotorClient(
            settings.mongo_host,
            settings.mongo_port
        )

        self._database = client['main']

        self._users = self._database['users']

    async def create_user(self, userInfo: UserInfo):
        r = await self._users.insert_one(
            userInfo.dict()
        )

    async def update_user(self, userInfo: UserInfo):
        a = await self._users.find_one(
            {'userID': userInfo.userID}
        )
        _id = a['_id']

        r = await self._users.update_one(
            {'_id': _id},
            {
                '$set': {**userInfo.dict()}
            }
        )

    async def get_user_info(self, user_id: int) -> UserInfo:
        r = await self._users.find_one(
            {
                'userID': user_id
            }
        )
        if r is None:
            return None

        r.pop('_id')

        userInfo = UserInfo(
            **r
        )
        return userInfo

    async def get_users(self, filter: dict) -> dict:
        # TODO Find only with subcription
        users = []
        async for r in self._users.find(filter):
            userInfo = UserInfo(
                userID=r['userID'],
                social=r['social'],
                course=r['course'],
                group=r['group'],
                place=r['place']
            )
            users.append(userInfo)

        return users


usersDB = UsersDB()