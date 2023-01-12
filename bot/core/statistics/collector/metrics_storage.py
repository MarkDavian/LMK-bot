import datetime
import os.path
from overrides import override

import pandas as pd

from config import settings
from bot.core.statistics.collector.errors import _StorageTypeError, _StorageFileError


class IMetricsStorage:
    def save(self, metric_name: str, *args) -> None:
        self._save_to_storage(metric_name, args)

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
        self.filepath = settings.metrics_filepath+'.csv'

        default_heads = [
            'Date', 'Time', 'Metric' # And then metrics
        ]
        metrics = settings.metrics['metrics']
        self.heads = default_heads + metrics

        self._accurate_csv_file()

    def _accurate_csv_file(self) -> None:
        if not os.path.isfile(self.filepath):
            print(
                f'No CSV file found in path ({self.filepath}). Trying to create file'
            )
            self._create_file()
        
    def _create_file(self):
        try:
            open(self.filepath, 'w').close()
        except Exception:
            raise _StorageFileError(f'Not able to create csv file ({self.filepath})')

    def _save_df(self, df: pd.DataFrame) -> None:
        df.to_csv(self.filepath, mode='a', header=False)

    @override
    def _save_to_storage(self, metric_name: str, *args) -> None:
        date = datetime.date.today().strftime('%Y-%m-%d')
        time = datetime.datetime.now(settings.tz_info).strftime('%H:%M:%S')
        data = [
            [date, time, metric_name, *args]
        ]
        
        df = pd.DataFrame(data, columns=self.heads)
        self._save_df(df)


class TextMetricsStorage(CSVMetricsStorage):
    def __init__(self) -> None:
        self.filepath = settings.metrics_filepath+'.txt'

        default_heads = [
            'Date', 'Time', 'Metric' # And then metrics
        ]
        metrics = settings.metrics['metrics']
        self.heads = default_heads + metrics

        self._accurate_csv_file()

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
        
        match storage_type:
            case 'CSV':
                return CSVMetricsStorage()
            case 'Mongo':
                return MongoMetricsStorage()
            case "Text":
                return TextMetricsStorage()