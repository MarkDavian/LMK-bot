import requests

from config import settings
from bot.core.scanner.site_parser import SiteParser


class Scanner:
    def __init__(self) -> None:
        self.interval = self._validate_interval(settings.scanner['time-interval'])

    def get_file_url(self):
        self._process_site()

        return self.result

    def _process_site(self):
        r = requests.get(self.url)
        html = r.text

        parser = SiteParser()
        parser.parse(html)

        self.check_result = parser.file_url
        if self.check_result != self.result:
            self.result = self.check_result
            return False

        return True

    def parse_site(self):
        r = requests.get(self.url)
        html = r.text

        parser = SiteParser()
        parser.parse(html)

        self.result = parser.file_url

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