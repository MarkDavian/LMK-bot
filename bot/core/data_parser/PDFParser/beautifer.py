
import pandas as pd


class CSVBeautifer:
    """Normalize CSV to pretend errors with parse
    """
    def __init__(self, csv_path: str) -> None:
        self.orig_csv = csv_path
        self.csv = 'right.csv'

    def beautify(self) -> pd.DataFrame:
        self.df = self._process()

        return self.df

    def _process(self) -> pd.DataFrame:
        self._search()
        df = pd.read_csv(self.csv)
        return df

    def _search(self):
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

