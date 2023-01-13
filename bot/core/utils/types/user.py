from shedule import GroupShedule


class UserInfo:
    """
    _id: ID in social network,
    _group: User group in school,
    _from: Place that is user from.
    """
    id: int
    group: str
    place: str
    social: str

    def __init__(self, group: str, place: str) -> None:
        self.group = group
        self.place = place


class User:
    info: UserInfo
    is_admin: bool
    shedule: GroupShedule

    def __init__(self, 
            userInfo: UserInfo,
            shedule: GroupShedule) -> None:
        self.info = userInfo
        self.shedule = shedule


