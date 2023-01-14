from datetime import timedelta, timezone
import json
from pydantic import BaseSettings


with open('settings/settings.json', 'rb') as file:
    settings_json = json.load(file)


_TZ_OFFSET = settings_json['timezone']['offset']
_TZ_NAME = settings_json['timezone']['name']


class Settings(BaseSettings):
    """Init of all settings
    """
    bot_api_key: str
    admin_id: int

    server_url: str
    tz_info = timezone(timedelta(hours=_TZ_OFFSET), name=_TZ_NAME) 

    metrics = settings_json['metrics']
    metrics_filepath = metrics['filepath']

    scanner = settings_json['site-scanner']


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
