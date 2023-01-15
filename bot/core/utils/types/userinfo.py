class UserInfo:
    """
    _id: ID in social network,
    _group: User group in school,
    _from: Place that is user from.
    """
    userID: int
    course: int
    group: str
    place: str
    social: str

    def __init__(self, userID: int, social: str, 
                course: int, group: str, place: str) -> None:
        self.userID = userID
        self.course = course
        self.group = group
        self.place = place
        self.social = social

    def dict(self) -> dict:
        return vars(self)

    def list(self) -> list:
        return [self.place, self.course, self.group, self.userID, self.social]