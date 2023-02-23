# usr/local/bin/python3
import argparse
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class SHEDULE_TIME:
    one = ('8:00', '9:30')
    two = ('9:40', '11:10')
    three = ('11:40', '13:10')
    hour = ('13:30', '14:10')
    four = ('13:30', '15:00')
    five = ('15:10', '16:40')
    six = ('16:50', '18:20')
    seven = ('18:30', '20:00')

    wed_four = ('14:20', '15:50')
    wed_five = ('16:00', '17:30')
    wed_six = ('17:40', '19:10')
    wed_seven = ('19:20', '20:50')

    SUBJECTS = [one, two, three, four, five, six, seven]
    WED_SUBJECTS = [one, two, three, wed_four, wed_five, wed_six, wed_seven]



class SheduleParser:
    def __init__(self, filepath: str) -> None:
        with open(filepath, 'r') as file:
            self.dict = json.load(file)

    async def parse(self) -> str:
        doc = self.dict

        for course, group in doc['Курс'].items():
            for group_name, shedule in group.items():
                for day, shed in shedule.items():
                    subjects = SHEDULE_TIME.SUBJECTS
                    for key, subject in shed.items():
                        try:
                            time = subjects[int(key)-1]
                        except ValueError:
                            time = SHEDULE_TIME.hour
                            subjects = SHEDULE_TIME.WED_SUBJECTS

                        doc['Курс'][course][group_name][day][key] = {
                            'Пара': subject,
                            'Время': time
                        }
        result = await self._save(doc)
        return result

    async def _save(doc: dict) -> str:
        filename = 'shedule.json'
        with open(filename, 'w') as file:
            json.dump(doc, file, ensure_ascii=False, indent=4)
        return filename