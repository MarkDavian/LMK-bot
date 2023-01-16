import logging


from config import settings

from bot.core.statistics.metrics.metrics_storage import (
    MetricsStorageFactory, 
    IMetricsStorage
)


metrics_logger = logging.getLogger(__name__)
metrics_logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"DataMaster.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
metrics_logger.addHandler(handler)


class Metrics():
    def __init__(self) -> None:
        metrics_logger.info('Initiating Metrics. Reading metrics fields')
        self.fields = settings.metrics['fields']

        metrics_logger.info('Getting storage')
        self.storage: IMetricsStorage = MetricsStorageFactory.get_storage(settings.metrics['storage'])

    def collect(self, metric_name: str, *args) -> None:
        """ONLY with fields in settings.json

        Args:
            metric_name (str): Metric name to store
            args: Metrics that provided in settings.json
        """
        metrics_logger.info('Collect new metrics')
        self.storage.save(metric_name, *args)


metrics = Metrics()
