import os

from pydantic_settings import BaseSettings


def to_bool(value: str) -> bool:
    """Convert string to boolean representations."""
    return value.lower() in ("true", "yes", "y", "1")


class AppSettings(BaseSettings):
    """App configurations."""
    APP_NAME: str = os.getenv("APP_NAME", "mypfa")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "debug").upper()
    LOG_USE_BASIC_FORMAT: bool = to_bool(os.getenv("LOG_USE_BASIC_FORMAT", "false"))
    LOG_DIR: str = os.getenv("LOG_DIR", "")
    LOG_FILE_ROTATION: str = os.getenv("LOG_FILE_ROTATION", "10 MB")
    LOG_FILE_RETENTION: str = os.getenv("LOG_FILE_RETENTION", "10 days")
    LOG_FILE_COMPRESSION: str = os.getenv("LOG_FILE_COMPRESSION", "gz")


class Settings(AppSettings):
    """Base configurations."""
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")


config = Settings()
