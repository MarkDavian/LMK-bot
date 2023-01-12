# from bot.core.statistics.collector.metrics_storage import (
#     CSVMetricsStorage,
#     MongoMetricsStorage,
#     TextMetricsStorage
# )

import pandas

heads = [
    'Date', 'time', 'Metric', 'Count'
]

data = [
    ['2022-12-01', '12:05:31','Get_shedule', '5'],
    ['2022-12-01', '12:06:12', 'Get_user', '2'],
    ['2022-12-01', '12:06:55', 'Count_shedule', '1']
]

df = pandas.DataFrame(data, columns=heads)

df.to_csv('file.csv')