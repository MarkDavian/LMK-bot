import logging
from typing import Optional

from bot.core.data_parser.PDFParser import PDFParser
from bot.core.utils.types.shedule import SHEDULE_TIME


json_parser_logger = logging.getLogger(__name__)
json_parser_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/JSONParser.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
json_parser_logger.addHandler(handler)
json_parser_logger.addHandler(logging.StreamHandler())


class JSONParser:
    def __init__(self, pdf_parser: Optional[PDFParser] = None,
                dict_to_parse: Optional[dict] = None) -> None:
        self.dict = dict_to_parse
        self.pdf_parser = pdf_parser

    def _get_dict(self):
        if self.dict is not None:
            return self.dict
        return self.pdf_parser.extract_dict()

    def parse(self):
        json_parser_logger.info('Start parsing doc')
        doc = self._get_dict()

        for course, shedule in doc['Курс'].items():
            for group_name, shed in shedule.items():
                for key, subject in shed.items():
                    time = SHEDULE_TIME.SUBJECTS[int(key[-1])-1]
                    if isinstance(subject, float):
                        subject = ""
                    doc['Курс'][course][group_name][key] = {
                        'Пара': subject,
                        'Время': time
                    }
        json_parser_logger.info('Doc parsed')
        return doc