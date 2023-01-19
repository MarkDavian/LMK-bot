import logging
import requests

from typing import Any
from urllib.parse import urlparse
from pathlib import Path

import tabula
import pandas as pd
from pydantic import BaseModel, validator

from bot.core.file_resolver.resolver import File

from .csv_parser import CSVParser
from .beautifer import CSVBeautifer


pdf_parser_logger = logging.getLogger(__name__)
pdf_parser_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/PDFParser.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
pdf_parser_logger.addHandler(handler)


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
        pdf_parser_logger.info('Starting PDF parser')
        src = FileSrc(path=src)
        filepath = src.path
        if self._is_url(filepath):
            filepath = self._download_file(filepath)

        output_csv = File('pdf-csv.csv')
        pdf_parser_logger.info('Start converting PDF to CSV')
        
        tabula.convert_into(filepath, output_csv, output_format="csv", pages='all')
        pdf_parser_logger.info('PDF converted')

        self.df = CSVBeautifer(output_csv).beautify()
        pdf_parser_logger.info('DataFrame is recieved')

        self.parser = CSVParser(dataframe=self.df)
        pdf_parser_logger.info('Start processing DataFrame')
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
        pdf_parser_logger.info(f'Downloading PDF file from {filepath}')

        path = File('changes.pdf')

        with open(path, 'wb') as file:
            r = requests.get(filepath)
            file.write(r.content)

        pdf_parser_logger.info(f'File {path} downloaded')

        return path
