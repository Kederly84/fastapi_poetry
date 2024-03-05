from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD'] = 'DEV'

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DRIVER: str
    SYNC_DRIVER: str
    SECRET_KEY: str
    ALGORITHM: str

    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_HOST: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    @property
    def database_url(self) -> str:
        return (f'{self.DRIVER}://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
                f'{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

    @property
    def sync_driver(self) -> str:
        return (f'{self.SYNC_DRIVER}://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
                f'{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

    @property
    def test_database_url(self) -> str:
        return (f'{self.DRIVER}://{self.TEST_POSTGRES_USER}:'
                f'{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOST}:'
                f'{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}')

    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/.env')

    # class Config:
    #     BASE_DIR = Path(__file__).resolve().parent.parent
    #     env_file = BASE_DIR / '.env'


settings = Settings()
