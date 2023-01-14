from typing import Optional
from bot.core.data_parser.PDFParser import PDFParser
from bot.core.utils.types.shedule import SHEDULE_TIME


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
        doc = self._get_dict()

        for course, shedule in doc['Курс'].items():
            for group_name, shed in shedule.items():
                for key, subject in shed.items():
                    time = SHEDULE_TIME.SUBJECTS[int(key)-1]
                    doc['Курс'][course][group_name][key] = {
                        'Пара': subject,
                        'Время': time
                    }
        return doc