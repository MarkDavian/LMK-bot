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
    def __init__(self, dict_to_parse: dict) -> None:
        self.dict = dict_to_parse

    def parse(self):
        print('Start parsing doc')
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
        print('Doc parsed')
        return doc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        'input', metavar='str', type=str,
        help='input file json')
    parser.add_argument(
        'output', metavar='str', type=str,
        help='output file')
    args = parser.parse_args()

    with open(args.input, 'r') as file:
        d = json.load(file)

    sp = SheduleParser(d)
    new_d = sp.parse()

    with open(args.output, 'w') as file:
        json.dump(new_d, file, indent=4, ensure_ascii=False)