from config import settings

from bot.core.statistics.collector.errors import _StorageTypeError


class BaseMetricsStorage:
    def save(self, metric_name: str, *args) -> None:
        ...


class CSVMetricsStorage(BaseMetricsStorage):
    ...


class MongoMetricsStorage(BaseMetricsStorage):
    ...


class TextMetricsStorage(BaseMetricsStorage):
    ...


class MetricsStorageFactory:
    @classmethod
    def get_storage(cls, storage_type: str) -> BaseMetricsStorage:
        if storage_type not in settings.metrics['available-storage-types']:
            raise _StorageTypeError(f'Storage type ({storage_type}) is not defined')
        
        match storage_type:
            case 'CSV':
                return CSVMetricsStorage()
            case 'Mongo':
                return MongoMetricsStorage()
            case "Text":
                return TextMetricsStorage()