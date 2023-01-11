from config import settings


class MetricsCollector:
    metrics: list[str]

    def __init__(self) -> None:
        self.metrics = settings.metrics['metrics']    

    def new_call(self, metric_name: str, **args) -> None:
        ...

    def new_metric(self, metric_name: str) -> None:
        ...