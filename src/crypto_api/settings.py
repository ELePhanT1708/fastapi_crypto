from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str
    server_port: int
    database_url: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
