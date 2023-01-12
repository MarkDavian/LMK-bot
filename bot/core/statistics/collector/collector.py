from config import settings

from bot.core.statistics.collector.metrics_storage import (
    _MetricNameError, 
    MetricsStorageFactory, 
    BaseMetricsStorage
)


class MetricsCollector:
    metrics: list[str]

    def __init__(self) -> None:
        self.metrics = settings.metrics['metrics']    
        self.storage: BaseMetricsStorage = MetricsStorageFactory.get_storage(settings.metrics['storage'])

    def new_call(self, metric_name: str, *args) -> None:
        if metric_name not in self.metrics:
            raise _MetricNameError(f'Metric name ({metric_name}) is not defined')

        self._save_metric(metric_name, args)

    def _save_metric(self, metric_name: str, *args) -> None:
        self.storage.save(metric_name, args)

    def new_metric(self, metric_name: str) -> None:
        self.metrics.append(metric_name)
