import os
from typing import Literal

from pydantic_settings import BaseSettings


def to_bool(value: str) -> bool:
    """Convert string to boolean representations."""
    return value.lower() in ("true", "yes", "y", "1")


class AgentSettings(BaseSettings):
    """ADK Agents configurations."""
    AGENT_DB_USER: str = os.getenv("AGENT_DB_USER", "pfa")
    AGENT_DB_PASSWORD: str = os.getenv("AGENT_DB_PASSWORD", "pfa")
    AGENT_DB_NAME: str = os.getenv("AGENT_DB_NAME", "pfa")
    AGENT_DB_HOST: str = os.getenv("AGENT_DB_HOST", "localhost")
    AGENT_DB_PORT: int = int(os.getenv("AGENT_DB_PORT", "5432"))
    AGENT_DB_PROVIDER: Literal["postgresql", "mysql"] = os.getenv(
        "AGENT_DB_PROVIDER", "postgresql"
    )
    AGENT_SESSION_SERVICE_URI: str = (
        f"{AGENT_DB_PROVIDER}+psycopg://{AGENT_DB_USER}:{AGENT_DB_PASSWORD}@"
        f"{AGENT_DB_HOST}:{AGENT_DB_PORT}/{AGENT_DB_NAME}"
    )
    AGENT_SERVE_WEB: bool = to_bool(os.getenv("AGENT_SERVE_WEB", "false"))


class MCPSettings(BaseSettings):
    """MCP configurations."""
    MCP_API_PREFIX: str = os.getenv("MCP_API_PREFIX", "/api/mcp")
    MCP_VERSION: str = os.getenv("MCP_VERSION", "v1")
    MCP_TRANSPORT: str = os.getenv("MCP_TRANSPORT", "http")
    MCP_REMOTE_HOST_URL: str = os.getenv("MCP_REMOTE_HOST_URL", "http://localhost")
    MCP_REMOTE_HOST_PORT: int = int(os.getenv("MCP_REMOTE_HOST_PORT", "7001"))


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


class LangsmithSettings(BaseSettings):
    """Langsmith configurations."""
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")


class GCPSettings(BaseSettings):
    """GCP resource-related configurations."""
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")
    GOOGLE_CSE_URL: str = os.getenv("GOOGLE_CSE_URL", "")
    GOOGLE_CSE_API_KEY: str = os.getenv("GOOGLE_CSE_API_KEY", "")
    GOOGLE_CSE_TIMEOUT: int = int(os.getenv("GOOGLE_CSE_TIMEOUT", "10"))

    GCS_BUCKET_ID: str = os.getenv("GCS_BUCKET_ID", "pfa-agents")


class Settings(AppSettings, LangsmithSettings, MCPSettings, GCPSettings, AgentSettings):
    """Base configurations."""
    HTTP_MAX_CONNECTIONS: int = int(os.getenv("HTTP_MAX_CONNECTIONS", "5"))
    HTTP_MAX_RETRIES: int = int(os.getenv("HTTP_MAX_RETRIES", "3"))

    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")


config = Settings()
