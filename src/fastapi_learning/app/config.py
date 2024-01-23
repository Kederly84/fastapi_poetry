from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DRIVER: str
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def database_url(self) -> str:
        return (f'{self.DRIVER}://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@{self.HOST}:'
                f'{self.PORT}/{self.POSTGRES_DB}')

    class Config:
        BASE_DIR = Path(__file__).resolve().parent.parent
        env_file = BASE_DIR / '.env'


settings = Settings()
