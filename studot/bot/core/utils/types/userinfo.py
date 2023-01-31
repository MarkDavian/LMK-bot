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

    shedule_notify: bool
    changes_notify: bool
    next_subject_notify: bool

    def __init__(self, userID: int, social: str, 
                course: Literal['1', '2', '3', '4'], 
                group: str, place: str, 
                shedule_notify=False,
                changes_notify=True,
                next_subject_notify=False,
                trial_expires: Optional[time] = None
    ) -> None:
        self.userID = userID
        self.course = course
        self.group = group
        self.place = place
        self.social = social

        self.shedule_notify = shedule_notify
        self.changes_notify = changes_notify
        self.next_subject_notify = next_subject_notify

        self.trial_expires = trial_expires

    def dict(self) -> dict:
        return vars(self)

    def list(self) -> list:
        """Only for metrics
        Listed attributes to store in csv etc.
        Returns:
            list
        """
        return [self.place, self.course, self.group, self.userID, self.social]