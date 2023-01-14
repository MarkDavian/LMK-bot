from shedule import GroupShedule

from userinfo import UserInfo


class User:
    info: UserInfo
    is_admin: bool
    shedule: GroupShedule

    def __init__(self, 
            userInfo: UserInfo,
            shedule: GroupShedule) -> None:
        self.info = userInfo
        self.shedule = shedule


