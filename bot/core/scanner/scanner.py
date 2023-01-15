import requests

from config import settings
from bot.core.scanner.site_parser import SiteParser


class Scanner:
    def __init__(self) -> None:
        self.result = ''
        self.check_result = ''
        self.interval = self._validate_interval(settings.scanner['time-interval'])
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

    def _process_site(self):
        r = requests.get(self.url)
        html = r.text

        parser = SiteParser()
        parser.parse(html)

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