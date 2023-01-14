class UserInfo:
    """
    _id: ID in social network,
    _group: User group in school,
    _from: Place that is user from.
    """
    id: int
    course: int
    group: str
    place: str
    social: str

    def __init__(self, group: str, place: str) -> None:
        self.group = group
        self.place = place