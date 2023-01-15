from typing import Any
import requests
from urllib.parse import urlparse
from pathlib import Path

import tabula
import pandas as pd
from pydantic import BaseModel, validator

from .csv_parser import CSVParser
from .beautifer import CSVBeautifer


class FileSrc(BaseModel):
    path: str

    @validator("path", pre=True)
    def validate_src(cls, value: Any) -> Any:
        url_parts = urlparse(value)
        is_url = True
        is_filepath = True

        if url_parts.scheme and url_parts.scheme != "http":
            is_url = False
        elif not Path(url_parts.path).exists():
            is_filepath = False

        if not is_url and not is_filepath:
            raise ValueError("src must be either existing local file path or HTTPS URL")

        return value


class PDFParser:
    def __init__(self, src: str) -> None:
        """Read PDF in filepath and processes it converting to CSV cells
        and then to pandas DataFrame

        Args:
            src (str): Path to PDF file or URL to file
        """
        src = FileSrc(path=src)
        filepath = src.path
        if self._is_url(filepath):
            filepath = self._download_file(filepath)

        output_csv = 'output.csv'

        tabula.convert_into(filepath, output_csv, output_format="csv", pages='all')
        self.df = CSVBeautifer(output_csv).beautify()

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

    def extract_json(self, output: str) -> str:
        return self.parser.json(output=output)

    def _is_url(self, filepath: str):
        return True

    def _download_file(self, filepath: str):
        path = 'file.pdf'
        with open(path, 'wb') as file:
            r = requests.get(filepath)
            file.write(r.content)
        return path
