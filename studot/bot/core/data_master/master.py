import logging
import json
import time

from bot.core.notifier.notifier import notifier

from bot.core.scanner.scanner import Scanner
from bot.core.data_parser.PDFParser import PDFParser
from bot.core.data_parser.JSONParser import JSONParser
from bot.core.file_resolver.resolver import File
from bot.core.utils.db.shedule import SheduleDB


"""Summary:
First of all, Scanner object scans site html and then provide PDFParser URL for download.
Then PDFParser will create a Pandas DataFrame that JSONParser will parse to Shedule format dict,
and save to SheduleDB in _change_shedule collection

DataMaster will observe for cached files, shedules to pretend over usage.
"""


master_logger = logging.getLogger(__name__)
master_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/DataMaster.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
master_logger.addHandler(handler)
master_logger.addHandler(logging.StreamHandler())


class DataMaster:
    def __init__(self) -> None:
        self.db = SheduleDB()
        self.scanner = Scanner()
        self.notifier = notifier
        self.time_interval = self.scanner.interval

    def start(self):
        try:
            master_logger.info('Data master started')
            while True:
                self._scan()
                self._check()
                master_logger.info(f'Sleeping {self.time_interval}s')
                time.sleep(self.time_interval)
        except Exception as er:
            master_logger.info('Data master stoped in cause of error')
            master_logger.error(er, exc_info=True)

    def _scan(self):
        master_logger.info('Scanning site')
        self.scanner.process()

    def _check(self):
        master_logger.info('Checking file url')
        if self.scanner.same_url:
            master_logger.info('Same file url')
            pass
        else:
            self._save()
            self._notify()

    def _save(self):
        master_logger.info('Saving changes to DB')
        jsonParser = JSONParser(PDFParser(src=self.scanner.result))
        changeShedule = jsonParser.parse()

        with open(File(f'changes_{self.scanner.date}.json'), 'w') as file:
            json.dump(changeShedule, file, ensure_ascii=False, indent=4, sort_keys=True)
        master_logger.info('JSON saved')

        self.db.save_change_shedule(change=changeShedule, date=self.scanner.date)
        master_logger.info('Document mongo saved')

    def _notify(self):
        self.notifier.notify_changes()


def start_data_master():
    master_logger.info('Starting data master')
    master = DataMaster()
    master.start()