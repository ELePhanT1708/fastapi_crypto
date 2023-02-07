from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    server_host: str = os.getenv('SERVER_HOST')
    server_port: int = os.getenv('SERVER_PORT')
    database_url: str = os.getenv('DATABASE_URL')
    binance_key: str = os.getenv('BINANCE_KEY')
    binance_secret: str = os.getenv('BINANCE_SECRET')

    class Config:
        env_file = 'config.env'
        env_file_encoding = 'utf-8'


settings = Settings()
