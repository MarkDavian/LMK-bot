from datetime import time
from typing import Literal, Optional, Union


class UserInfo:
    """
    userID: ID in social network,
    group: User group in school,
    place: Place that is user from.
    """
    userID: int
    course: Literal['1', '2', '3', '4']
    group: str
    place: str
    social: str

    subcribe: Union[float, None] # Unix timestamp where subcribe will be expired

    shedule_notify: bool = False
    changes_notify: bool = True
    next_subject_notify: bool = False

    def __init__(self, userID: int, social: str, 
                course: Literal['1', '2', '3', '4'], 
                group: str, place: str, 
                trial: Optional[time] = None) -> None:
        self.userID = userID
        self.course = course
        self.group = group
        self.place = place
        self.social = social

        self.trial_expires = trial

    def dict(self) -> dict:
        return vars(self)

    def list(self) -> list:
        """Only for metrics
        Listed attributes to store in csv etc.
        Returns:
            list
        """
        return [self.place, self.course, self.group, self.userID, self.social]