from bot.core.utils.db.users import UsersDB

from bot.core.utils.types.user import UserInfo

from bot.core.statistics.metrics.metrics import metrics


class CollectorProxy_UsersDB:
    def __init__(self, db: UsersDB) -> None:
        self.db = db

    async def create_user(self, userInfo: UserInfo):
        await metrics.collect('new_user', *userInfo.list())
        return await self.db.create_user(userInfo)

    async def get_user_info(self, user_id: int):
        return await self.db.get_user_info(user_id)

    async def update_user(self, userInfo: UserInfo):
        await metrics.collect('update_user', *userInfo.list())
        return await self.db.update_user(userInfo)

usersDB = CollectorProxy_UsersDB(UsersDB())