class UserInfo:
    group: str
    place: str

    def __init__(self, group: str, place: str) -> None:
        self.group = group
        self.place = place


class User:
    """
    _id: ID in social network,
    _group: User group in school,
    _from: Place that is user from.
    """
    _id: int
    group: str
    place: str

    is_admin: bool

    def __init__(self, 
            id: int, 
            userInfo: UserInfo) -> None:
        self._id = id
        self.group = userInfo.group
        self.place = userInfo.place


