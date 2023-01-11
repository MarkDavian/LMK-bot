from config import settings


class _MetricNameError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return super().__str__()


class BaseMetricsStorage:
    ...


class CSVMetricsStorage(BaseMetricsStorage):
    ...


class MongoMetricsStorage(BaseMetricsStorage):
    ...


class TextMetricsStorage(BaseMetricsStorage):
    ...


class MetricsCollector:
    metrics: list[str]

    def __init__(self) -> None:
        self.metrics = settings.metrics['metrics']    
        self.storage = settings.metrics['storage']

    def new_call(self, metric_name: str, *args) -> None:
        if metric_name not in self.metrics:
            raise _MetricNameError(f'Metric name ({metric_name}) is not defined')

        self._save_metric(metric_name, args)

    def _save_metric(self, metric_name: str, *args) -> None:
        ...

    def new_metric(self, metric_name: str) -> None:
        self.metrics.append(metric_name)
