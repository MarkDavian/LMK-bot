import json
import os
import pandas as pd


class MainSheduleParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

        df = pd.read_excel(filepath)
        df.to_json('jason.json', force_ascii=False)

        with open('jason.json', 'r') as file:
            self.r = json.load(file)
            self.r.pop('день')
            self.r.pop('пара')

        with open('tmp.json', 'w') as file:
            json.dump(self.r, file, ensure_ascii=False, indent=4)

        os.remove('jason.json')

    async def _get_day(self, num: int) -> str:
        if num < 7:
            return 'Понедельник'
        elif num < 14:
            return 'Вторник'
        elif num < 21:
            return 'Среда'
        elif num < 28:
            return 'Четверг'
        elif num < 35:
            return 'Пятница'
        else:
            return 'Суббота'
        
    async def parse(self) -> None:
        next = {}
        for group, shed in self.r.items():
            day_dict = {
                'Понедельник': {}, 'Вторник': {},
                'Среда': {},       'Четверг': {},
                'Пятница': {},     'Суббота': {},
            }
            para_count = 1
            for num, string in shed.items():
                if string is None:
                    string = ""

                string.strip()
                string.rstrip()

                if 'КЛАССНЫЙ ЧАС' in string:
                    day_dict[self._get_day(int(num))]['Кл. час'] = string
                else:
                    day_dict[self._get_day(int(num))][para_count] = string
                    if day_dict[self._get_day(int(num))][para_count] == "":
                        day_dict[self._get_day(int(num))].pop(para_count)
                    para_count += 1

                if para_count > 7:
                    para_count = 1
        

            next[group] = day_dict

        final = 'final.json'
        tmp = 'tmp.json'
        with open(final, "w") as file:
            json.dump(next, file, ensure_ascii=False, indent=4)

        return final, tmp