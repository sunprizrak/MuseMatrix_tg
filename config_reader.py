from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    web_server_host: str
    web_server_port: int
    webhook_path: str
    webhook_secret: str
    base_webhook_url: str
    host_name: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


config = Settings()