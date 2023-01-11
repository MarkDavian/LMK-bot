from dataclasses import dataclass
from user import UserInfo


@dataclass(frozen=True)
class _SHEDULE_DAY:
    monday = 'Понедельник'
    tuesday = 'Вторник'
    wednesday = 'Среда'
    thursday = 'Четверг'
    friday = 'Пятница'
    saturday = 'Суббота'
    sunday = 'Воскресенье'


class Subject:
    """Subject class for representive subjects

    Attributes:
        name (str): Group name
        time (str): Time in string when subject to start
    """

    name: str
    time: str

    def __init__(self, name: str, time) -> None:
        self.name = name
        self.time = time

    def __str__(self) -> str:
        return self.__dict__().__str__()

    def __repr__(self) -> str:
        return self.__dict__().__str__()

    def __dict__(self) -> dict:
        return {
            "Предмет": self.name,
            "Время": self.time
        }


class DayShedule:
    """Represent of a day shedule

    Attributes:
        name (str): Day name of the week
        subjects (lits[Subject]): List of subjects by a day
    """

    _name: str
    _subjects: list[Subject]

    def __init__(self, day: _SHEDULE_DAY, subjects: list[Subject]) -> None:
        self._name = day
        self._subjects = subjects

    @property
    def name(self) -> str:
        return self._name

    @property
    def subjects(self) -> list[Subject]:
        return self._subjects

    def dict(self):
        keys = [i for i in range(1, 1+len(self._subjects))]
        new_dict = dict(zip(keys, self._subjects))

        return new_dict

    def __repr__(self) -> str:
        return self.dict()


class WeekShedule:
    """
    Represent of a week shedule.
    This is a list of DayShedule
    """

    def __init__(self, days_shedule: list[DayShedule]) -> None:
        days = [day.name for day in days_shedule]
        shedule = [day_shed.dict() for day_shed in days_shedule]

        self.week_shedule = dict(zip(days, shedule))

    def dict(self) -> dict:
        return self.week_shedule

    def day(self, day: str) -> DayShedule:
        return self.week_shedule[day]

    def days_with(self, subject: str):
        con = {}
        for day, shedule in self.week_shedule.items():
            for sub in shedule.values():
                if sub.name == subject:
                    con[day] = shedule
                    break
        return con


class GroupShedule:
    """Represent User group info

    Attributes:
        group (str): Group name
        place (str): Place where group from
        shedule (WeekShedule): Shedule for a week for that group
    """

    group: str
    place: str
    shedule: WeekShedule

    def __init__(self, userInfo: UserInfo, shedule: WeekShedule) -> None:
        self.group = userInfo.group
        self.place = userInfo.place
        self.shedule = shedule

    def get_shedule_for(self, day: _SHEDULE_DAY) -> DayShedule:
        shedule = self.shedule.day(day)
        return shedule

    def days_with_subject(self, subject: str) -> WeekShedule:
        shedule = self.shedule.days_with(subject)
        return shedule

    def dict(self):
        d = {
            'Группа': self.group,
            'Место': self.place,
            'Расписание': self.shedule.dict()
        }
        return d


class WeekSheduleFactory:
    """Needs to build WeekShedule from a dict
    """

    def __init__(self, document: dict) -> None:
        days = []
        for day, shedule in document.items():
            days.append(
                DayShedule(
                    day=day,
                    subjects=[
                        Subject(sub['Предмет'], sub['Время']) 
                        for sub in shedule.values()
                    ]
                )
            )
        self.weekShedule = WeekShedule(days)

    def get_week_shedule(self) -> WeekShedule:
        return self.weekShedule


class GroupSheduleFactory:
    """Needs to build GroupShedule from a dict
    """
    def __init__(self, document: dict) -> None:
        userInfo = UserInfo(
                group=document['Группа'],
                place=document['Место']
        )
        weekShedule = WeekSheduleFactory(document['Расписание']).get_week_shedule()

        self.group_shedule = GroupShedule(
            userInfo=userInfo,
            shedule=weekShedule
        )

    def get_group_shedule(self) -> GroupShedule:
        return self.group_shedule
