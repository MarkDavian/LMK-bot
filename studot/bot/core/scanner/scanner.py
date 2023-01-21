import requests
import logging

from config import settings
from bot.core.scanner.site_parser import SiteParser


scanner_logger = logging.getLogger(__name__)
scanner_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/Scanner.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
scanner_logger.addHandler(handler)
scanner_logger.addHandler(logging.StreamHandler())


class Scanner:
    result: str
    date: str

    def __init__(self) -> None:
        scanner_logger.info('Init Scanner. Reading time interval from settings')
        self.result = ''
        self.check_result = ''
        self.interval = self._validate_interval(settings.scanner['time-interval'])
        scanner_logger.info('Done')
        self.url = 'http://www.lmk-lipetsk.ru/main_razdel/shedule/index.php'

    def get_file_url(self):
        self._process_site()

        return self.result

    def process(self):
        self._process_site()

    def parse_site(self):
        r = requests.get(self.url)
        html = r.text

        parser = SiteParser()
        parser.parse(html)

        self.result = parser.file_url
        self.date = parser.date

    def _process_site(self):
        scanner_logger.info('Start processing site. Getting html')
        r = requests.get(self.url)
        html = r.text

        scanner_logger.info('Start parsing html')
        parser = SiteParser()
        parser.parse(html)
        self.date = parser.date

        scanner_logger.info('Done')

        self.check_result = parser.file_url
        if self.check_result != self.result:
            self.same_url = False
            self.result = self.check_result
        else:
            self.same_url = True

    # TODO Create validation
    def _validate_interval(self, string: str):
        """Validates time interval in format <TT S>
        Where T - time interval
        Where S - symbol representing (h, m, s)
        """
        s = string.split()
        value = int(s[0])
        sym = s[1]

        if sym == 'h':
            value = value * 60 * 60
        elif sym == 'm':
            value = value * 60

        seconds_interval = value

        return seconds_interval