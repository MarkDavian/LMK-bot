import logging

from prometheus_client import Gauge

from config import settings

from bot.core.statistics.metrics.metrics_storage import (
    MetricsStorageFactory, 
    IMetricsStorage
)


"""Metrics
Metrics divided into users metrics and software metrics
"""


metrics_logger = logging.getLogger(__name__)
metrics_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/Metrics.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
metrics_logger.addHandler(handler)
metrics_logger.addHandler(logging.StreamHandler())


class Metrics:
    def __init__(self) -> None:
        metrics_logger.info('Initiating Metrics. Reading metrics fields')
        self.settings = settings.metrics
        self.fields = self.settings['fields']
        
        self.gauges = {}
        self._metrics = {}

        metrics_logger.info('Getting storage')
        self.storage: IMetricsStorage = MetricsStorageFactory.get_storage(settings.metrics['storage'])

    async def collect(self, metric_name: str, *args) -> None:
        """ONLY with fields in settings.json

        Args:
            metric_name (str): Metric name to store
            args: Metrics that provided in settings.json
        """
        metrics_logger.info('Collect new metrics')
        await self.export(metric_name, *args)
        await self.storage.save(metric_name, *args)

    async def export(self, metric_name: str, *args) -> None:
        await self._create_gauge(metric_name, *args)
        await self._set_gauge_value(metric_name)
    
    async def gauge(self, metric_name: str, value: int):
        if self.gauges.get(metric_name) is None:
            self.gauges[metric_name] = Gauge(metric_name, "User Metric")
        self.gauges[metric_name].set(value)

    async def _create_gauge(self, metric_name: str, *args) -> None:
        if self.gauges.get(metric_name) is None:
            self.gauges[metric_name] = Gauge(metric_name, "Collectable user stats")
            self._metrics[metric_name] = 1
        else:
            self._metrics[metric_name] += 1

    async def _set_gauge_value(self, metric_name: str) -> None:
        value = self._metrics[metric_name]
        self.gauges[metric_name].set(value)
    


metrics = Metrics()
