import datetime
import os.path
import logging

from overrides import override

import pandas as pd

from config import settings
from bot.core.statistics.metrics.errors import _StorageTypeError, _StorageFileError


metrics_storage_logger = logging.getLogger(__name__)
metrics_storage_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/MetricsStorage.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
metrics_storage_logger.addHandler(handler)
metrics_storage_logger.addHandler(logging.StreamHandler())


class IMetricsStorage:
    def save(self, metric_name: str, *args) -> None:
        self._save_to_storage(metric_name, *args)

    def new_metric(self, metric_name: str) -> None:
        self._create_new_metric(metric_name)

    def _save_to_storage(self, metric_name: str, *args) -> None:
        """BaseMetricsStorage childs must to ovveride this method"""
        ...


class CSVMetricsStorage(IMetricsStorage):
    """
    CSVMetricsStorage init with creating filepath to csv file and 
    writing to self the metrics names to provide the csv table heads.

    If file '.csv' is not exist attempting about this and tryies to create one.
    """

    def __init__(self) -> None:
        """Get CSV file heads with metrcis
        """
        self._init_filepath()

        metrics_storage_logger.info('Getting metrics fiedls from settings')
        metrics = settings.metrics['fields']
        self.heads = [
            'Date', 'Time', 'Metric'
        ]
        self.heads += metrics

        self._accurate_csv_file()

    def _init_filepath(self) -> None:
        metrics_storage_logger.info('Getting filepath')
        self.filepath = settings.metrics_filepath+'.csv'

    def _accurate_csv_file(self) -> None:
        metrics_storage_logger.info('Checking csv path file exist')
        if not os.path.isfile(self.filepath):
            print(
                f'No CSV file found in path ({self.filepath}). Trying to create file'
            )
            self._create_file()
        
    def _create_file(self):
        try:
            metrics_storage_logger.info('Creating file')
            pd.DataFrame([], columns=self.heads).to_csv(self.filepath, header=True)
            print(
                f'CSV file in path ({self.filepath}) created'
            )
        except Exception:
            metrics_storage_logger.error('File was not created', exc_info=True)
            raise _StorageFileError(f'Not able to create csv file ({self.filepath})')

    def _save_df(self, df: pd.DataFrame) -> None:
        metrics_storage_logger.info('Saving DataFrame to CSV')
        df.to_csv(self.filepath, mode='a', header=False)
        metrics_storage_logger.info('DataFrame is saved')

    @override
    def _save_to_storage(self, metric_name: str, *args) -> None:
        date = datetime.date.today().strftime('%Y-%m-%d')
        time = datetime.datetime.now(settings.tz_info).strftime('%H:%M:%S')
        data = [
            [date, time, metric_name, *args]
        ]
        metrics_storage_logger.info(f'Got metrics {data}')

        df = pd.DataFrame(data, columns=self.heads)
        self._save_df(df)


class TextMetricsStorage(CSVMetricsStorage):
    def __init__(self) -> None:
        super().__init__()

    @override
    def _init_filepath(self) -> None:
        self.filepath = settings.metrics_filepath+'.txt'

    @override
    def _save_df(self, df: pd.DataFrame) -> None:
        df.to_csv(self.filepath, mode='a', header=False, sep=', ')


class MongoMetricsStorage(IMetricsStorage):
    @override
    def _save_to_storage(self, metric_name: str, *args) -> None:
        ...


class MetricsStorageFactory:
    @classmethod
    def get_storage(cls, storage_type: str) -> IMetricsStorage:
        if storage_type not in settings.metrics['available-storage-types']:
            raise _StorageTypeError(f'Storage type ({storage_type}) is not defined')
        
        if storage_type == 'CSV':
            metrics_storage_logger.info('Initiate CSV storage')
            return CSVMetricsStorage()
        elif storage_type == 'Mongo':
            metrics_storage_logger.info('Initiate Mongo storage')
            return MongoMetricsStorage()
        elif storage_type == 'Text':
            metrics_storage_logger.info('Initiate Text storage')
            return TextMetricsStorage()