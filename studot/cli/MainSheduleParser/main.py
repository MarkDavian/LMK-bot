import json
import os
import pandas as pd

df = pd.read_excel('4_curs.xlsx')

df.to_json('jason.json', force_ascii=False)

with open('jason.json', 'r') as file:
    r = json.load(file)

os.remove('jason.json')

r.pop('день')
r.pop('пара')

next = {}

def get_day(num):
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

for group, shed in r.items():
    day_dict = {
        'Понедельник': {},
        'Вторник': {},
        'Среда': {},
        'Четверг': {},
        'Пятница': {},
        'Суббота': {},
    }
    para_count = 1
    for num, string in shed.items():
        if string is None:
            string = ""

        string.strip()
        string.rstrip()

        if 'КЛАССНЫЙ ЧАС' in string:
            day_dict[get_day(int(num))]['Кл. час'] = string
        else:
            day_dict[get_day(int(num))][para_count] = string
            if day_dict[get_day(int(num))][para_count] == "":
                day_dict[get_day(int(num))].pop(para_count)
            para_count += 1


        if para_count > 7:
            para_count = 1
        

    next[group] = day_dict


# with open('next.json', 'w') as file:
#     json.dump(r, file, ensure_ascii=False, indent=4)


# with open('result.json', 'w') as file:
#     json.dump(next, file, ensure_ascii=False, indent=4)


# with open('result.json', 'r') as var, open("final.json", "w") as file:
#     for line in var:
#         line = line.rstrip()
#         file.write(line)

# with open('final.json', 'r') as file:
#     r = json.load(file)

with open('final.json', "w") as file:
    json.dump(next, file, ensure_ascii=False, indent=4)