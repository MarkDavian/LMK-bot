import json
from pydantic import BaseSettings


with open('settings/metrics.json', 'rb') as file:
    metrics_json = json.load(file)


class Settings(BaseSettings):
    """Init of all settings
    """
    bot_api_key: str
    admin_id: int
    server_url: str

    metrics = metrics_json
    metrics_filepath = 'database/metrics/metrics'


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
