from pydantic import BaseSettings


class Settings(BaseSettings):
    """Init of all settings
    """
    bot_api_key: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()