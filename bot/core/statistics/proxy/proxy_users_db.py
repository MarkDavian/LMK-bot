from bot.core.utils.db.users import UsersDB

from bot.core.utils.types.user import UserInfo

from bot.core.statistics.metrics.metrics import metrics


class CollectorProxy_UsersDB:
    def __init__(self, db: UsersDB) -> None:
        self.db = db

    def create_user(self, userInfo: UserInfo):
        metrics.collect('New user', userInfo.place, userInfo.group, userInfo.id, userInfo.social)
        return self.db.create_user(userInfo)

usersDB = CollectorProxy_UsersDB(UsersDB())