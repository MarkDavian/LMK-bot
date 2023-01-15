from bot.core.scanner.site_parser import SiteParser
from bot.core.data_parser.PDFParser import PDFParser
from bot.core.data_parser.JSONParser import JSONParser
from bot.core.utils.db.shedule import SheduleDB


"""Summary:
First of all, Scanner object scans site html and then provide PDFParser URL for download.
Then PDFParser will create a Pandas DataFrame that JSONParser will parse to Shedule format dict,
and save to SheduleDB in _change_shedule collection

DataOperator will observe for cached files, shedules to pretend over usage.
"""


class DataMaster:
    def __init__(self) -> None:
        ...