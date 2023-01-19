from typing import Literal


class UserInfo:
    """
    _id: ID in social network,
    _group: User group in school,
    _from: Place that is user from.
    """
    userID: int
    course: Literal['1', '2', '3', '4']
    group: str
    place: str
    social: str

    def __init__(self, userID: int, social: str, 
                course: Literal['1', '2', '3', '4'], 
                group: str, place: str) -> None:
        self.userID = userID
        self.course = course
        self.group = group
        self.place = place
        self.social = social

    def dict(self) -> dict:
        return vars(self)

    def list(self) -> list:
        """Only for metrics
        Listed attributes to store in csv etc.
        Returns:
            list
        """
        return [self.place, self.course, self.group, self.userID, self.social]