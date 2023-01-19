import datetime
import logging

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


site_parser_logger = logging.getLogger(__name__)
site_parser_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/SiteParser.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
site_parser_logger.addHandler(handler)


class SiteParser:
    """Scans HTML for <a> tag href with file url
    """
    url: str
    file_url: str
    date: str

    def parse(self, html_text: str):
        """Find exactly 
        """
        site_parser_logger.info('Getting started to parse html')
        soup = BeautifulSoup(html_text, features="html5lib")
        file = soup.find(
            'div', {'class': 'right-column'}
        ).find(
            'div', {'class': 'page-tmpl-content'}
        ).find_all(
            'h2'
        )[0].find(
            'a'
        ).get('href')
        
        self.file_url = 'http://www.lmk-lipetsk.ru/'+file
        self.date = self.find_date(soup)
        
        site_parser_logger.info('html parsed')

    def find_date(self, soup: BeautifulSoup) -> str:
        date = soup.find(
            'div', {'class': 'right-column'}
        ).find(
            'div', {'class': 'page-tmpl-content'}
        ).find_all(
            'h2'
        )[0].find(
            'a'
        ).find(
            'span'
        ).text
        
        date = date.split()[-1]
        date = date.split('.')
        date = [int(d) for d in date]
        date = datetime.date(date[2], date[1], date[0]).strftime('%Y-%m-%d')

        return date
