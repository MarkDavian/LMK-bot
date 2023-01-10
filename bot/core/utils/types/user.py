class Group:
    name: str
    place: str

    def __init__(self, name: str, place: str) -> None:
        self.name = name
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
            group: Group) -> None:
        self._id = id
        self.group = group.name
        self.place = group.place


