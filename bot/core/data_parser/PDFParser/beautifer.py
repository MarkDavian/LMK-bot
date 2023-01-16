import logging
import pandas as pd

from bot.core.file_resolver.resolver import File


beautifer_logger = logging.getLogger(__name__)
beautifer_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"DataMaster.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
beautifer_logger.addHandler(handler)


class CSVBeautifer:
    """Normalize CSV to pretend errors with parse
    """
    def __init__(self, csv_path: str) -> None:
        beautifer_logger.info('Recieve csv path')
        self.orig_csv = csv_path
        self.csv = File('beauty.csv')
        beautifer_logger.info('Destination csv created')

    def beautify(self) -> pd.DataFrame:
        beautifer_logger.info('Start processing csv')
        self.df = self._process()

        return self.df

    def _process(self) -> pd.DataFrame:
        self._search()
        beautifer_logger.info('Reading csv to DataFrame')
        df = pd.read_csv(self.csv)
        beautifer_logger.info('DataFrame read')
        return df

    def _search(self):
        beautifer_logger.info('Start beautifing')
        def right_line(line: str):
            spec_sym = ('"', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я')
            if line.lower().startswith(spec_sym) or 'курс' in line.lower():
                return True
            return False

        with open(self.orig_csv, 'r') as f1, open(self.csv, 'w') as f2:
            lines = f1.readlines()
            f2_lines = []

            for c, line in enumerate(lines):
                line = line.strip()
                if not right_line(line):
                    line = '"",'+line[:-1]
                elif 'практика' in line.lower():
                    break
                    

                # f2_lines.append(line)
                f2.write(line+'\n')
                
        beautifer_logger.info('Beautifing done')
