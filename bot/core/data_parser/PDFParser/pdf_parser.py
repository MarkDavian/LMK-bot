import tabula
import pandas as pd

from .csv_parser import CSVParser


class PDFParser:
    def __init__(self, filepath: str) -> None:
        """Read PDF in filepath and processes it converting to CSV cells
        and then to pandas DataFrame

        Args:
            filepath (str): Path to PDF file
        """
        self.filepath = filepath
        dfs = tabula.read_pdf(self.filepath, pages='all')
        self.df = dfs[0]
        self.parser = CSVParser(dataframe=self.df)
        self.parser.process()

    def extract_csv(self, output: str) -> str:
        """Read PDF and extract csv cells to file in <output> path

        Args:
            output (str): Output csv file path

        Returns:
            str: Output filepath
        """
        self.df.to_csv(output)
        return output

    def extract_df(self) -> pd.DataFrame:
        return self.df

    def extract_dict(self) -> dict:
        return self.parser.dict()

    def extract_json(self) -> str:
        return self.parser.json()

