from datetime import timedelta, timezone
import yaml
from pydantic import BaseSettings

try:
    with open('settings/settings.yml', 'rb') as file:
        settings_yml = yaml.safe_load(file)
        settings_yml = settings_yml['app']
except:
    print('No settings file. Use default settings')
    settings_yml = {
        'timezone': {
            'name': 'MSC',
            'offset': 3
        },
        'metrics': {
            'filepath': 'data/metrics/metrics',
            'fields': ['Place', 'Course',
                       'Group', 'UserId',
                       'Social'],
            'timing': True,
            'storage': 'CSV',
            'available-storage-types': [
                'CSV', 'Mongo', 'Text'
            ],
            'export-port': 9877
        },
        'site-scanner': {
            'time-interval': '10 m'
        },
        'files': {
            'path': 'files/',
            'max-count': 10
        }
    }


_TZ_NAME = settings_yml['timezone']['name']
_TZ_OFFSET = settings_yml['timezone']['offset']


class Settings(BaseSettings):
    """Init of all settings
    """
    bot_api_key: str
    vk_bot_api_key: str
    admin_id: int

    mongo_host: str

    mongo_port: int

    server_url: str
    tz_info = timezone(timedelta(hours=_TZ_OFFSET), name=_TZ_NAME) 

    metrics = settings_yml['metrics']
    metrics_filepath = metrics['filepath']

    scanner = settings_yml['site-scanner']

    files = settings_yml['files']


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
