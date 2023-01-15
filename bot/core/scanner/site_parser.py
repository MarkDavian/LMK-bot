import requests
from bs4 import BeautifulSoup

# from bot.core.utils.types.shedule import SHEDULE_DAY

# SITE = 'http://www.lmk-lipetsk.ru/'
# CHANGE = '000/'

# def create_change_file_url():
#     date = datetime.date.today()
#     day = date.day
#     day_name = SHEDULE_DAY.MONTHS[date.month-1][:-1].lower() + 'я'

#     change = CHANGE+f'{day}%20{day_name}.pdf'

#     print(change)



class SiteParser:
    """Scans HTML for <a> tag href with file url
    """
    url: str
    file_url: str

    def parse(self, html_text: str):
        """Find exactly 
        """
        soup = BeautifulSoup(html_text, features="html5lib")
        file = soup.find(
            'div', {'class': 'right-column'}
        ).find(
            'div', {'class': 'page-tmpl-content'}
        ).find_all(
            'h2'
        )[1].find(
            'a'
        ).get('href')
        
        self.file_url = 'http://www.lmk-lipetsk.ru/'+file