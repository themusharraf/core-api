from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_NAME: str = "Coffee API"
    APP_AUTHOR: str = "Musharraf DEV"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Coffee Shop API"
    APP_DEBUG: bool = False

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    EMAIL_FROM: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    SECRET_KEY: SecretStr
    REFRESH_TOKEN_EXPIRE_DAYS: int = 60 * 24
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 2
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Config()
settings.DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
