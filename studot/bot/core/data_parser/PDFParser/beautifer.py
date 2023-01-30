import logging
import pandas as pd

from bot.core.file_resolver.resolver import File


beautifer_logger = logging.getLogger(__name__)
beautifer_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/CSVBeautifer.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
beautifer_logger.addHandler(handler)
beautifer_logger.addHandler(logging.StreamHandler())


class CSVBeautifer:
    """Normalize CSV to pretend errors with parse
    """
    def __init__(self, csv_path: str) -> None:
        beautifer_logger.info('Recieve csv path')
        self.orig_csv = csv_path
        self.csv = File('beauty.csv')
        beautifer_logger.info('Destination csv created')

    def beautify(self) -> pd.DataFrame:
        """Doc type finder
        If doc has more field than limited doc
        then process it to limited version and then
        process as default
        """
        beautifer_logger.info('Start processing csv')
        is_limited = self._check_limited()

        if not is_limited:
            beautifer_logger.info('CSV type is not limited. Getting start to limit it')
            self._make_limited()

        self.df = self._process()

        return self.df

    def _check_limited(self) -> bool:
        with open(self.orig_csv, 'r') as f1:
            line = f1.readlines()[0]
            line.strip()
            # line = line[0].split(",")

        if "Заменить" in line:
            return False
        return True        

    def _make_limited(self) -> None:
        df = pd.read_csv(self.orig_csv)
        df = df.drop(columns=['Заменить'])
        df.to_csv(self.orig_csv, index=False)

    def _process(self) -> pd.DataFrame:
        self._beautifing()
        beautifer_logger.info('Writing csv to DataFrame')
        df = pd.read_csv(self.csv)
        beautifer_logger.info('DataFrame was written')
        return df

    def _beautifing(self):
        beautifer_logger.info('Start beautifing')
        def right_line(line: str):
            spec_sym = ('"', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я')
            if line.lower().startswith(spec_sym) or 'курс' in line.lower():
                return True
            return False

        with open(self.orig_csv, 'r') as f1, open(self.csv, 'w') as f2:
            lines = f1.readlines()

            for c, line in enumerate(lines):
                line = line.strip()
                if not right_line(line):
                    if line[0] == ',':
                        if line[-1] == ',':
                            line = '""'+line[:-1]
                        else:
                            line = '""'+line
                    else:    
                        if line[-1] == ',':
                            line = '"",'+line[:-1]
                        else:
                            line = '"",'+line
                elif 'практика' in line.lower():
                    break
                    

                f2.write(line+'\n')
                
        beautifer_logger.info('Beautifing done')

def start_process():
    c = CSVBeautifer('file.csv')
    df = c.beautify()