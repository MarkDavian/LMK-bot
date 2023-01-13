from config import settings

from bot.core.statistics.metrics.metrics_storage import (
    MetricsStorageFactory, 
    IMetricsStorage
)


class Metrics():
    def __init__(self) -> None:
        self.fields = settings.metrics['fields']
        self.storage: IMetricsStorage = MetricsStorageFactory.get_storage(settings.metrics['storage'])

    def collect(self, metric_name: str, *args) -> None:
        """ONLY with fields in settings.json

        Args:
            metric_name (str): Metric name to store
            args: Metrics that provided in settings.json
        """
        self.storage.save(metric_name, *args)


metrics = Metrics()
