from config import settings

from bot.core.statistics.collector.errors import _MetricNameError
from bot.core.statistics.collector.metrics_storage import (
    MetricsStorageFactory, 
    IMetricsStorage
)


class MetricsCollector:
    metrics: list[str]

    def __init__(self) -> None:
        self.metrics = settings.metrics['metrics']    
        self.storage: IMetricsStorage = MetricsStorageFactory.get_storage(settings.metrics['storage'])

    def collect_new(self, metric_name: str, *args) -> None:
        if metric_name not in self.metrics:
            raise _MetricNameError(f'Metric name ({metric_name}) is not defined')

        self._save_metric(metric_name, args)

    def _save_metric(self, metric_name: str, *args) -> None:
        self.storage.save(metric_name, args)

