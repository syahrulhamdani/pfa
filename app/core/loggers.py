"""Logger module using Loguru's native structured logging capabilities."""

import json
import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from app.core.config import config as c


def structurize_log(
    message, service_name: str = "", service_version: str = ""
) -> str:
    record = message.record
    log_record = {
        "time": record["time"].isoformat(),
        "severity": record["level"].name,
        "process_id": record["process"].id,
        "process_name": record["process"].name,
        "thread_id": record["thread"].id,
        "thread_name": record["thread"].name,
        "logger": record["name"],
        "function": record["function"],
        "line": record["line"],
        "message": record["message"],
        "extra": {
            "service_name": c.APP_NAME or "",
            "service_version": c.APP_VERSION or "",
            **record.get("extra", {}),
        }
    }

    # Handle exceptions if present
    if record.get("exception"):
        exc = record["exception"]
        exc_info = {
            "type": str(getattr(exc, "type", type(exc).__name__)),
            "value": str(getattr(exc, "value", exc)),
        }
        # Only add traceback if it exists
        if hasattr(exc, "traceback") and exc.traceback is not None:
            exc_info["traceback"] = exc.traceback.format_exc()
        log_record["exception"] = exc_info

    print(json.dumps(log_record, default=str), file=sys.stderr, flush=True)


def setup_loggers(
    log_level: str = c.LOG_LEVEL,
    use_basic_format: bool = c.LOG_USE_BASIC_FORMAT,
) -> None:
    """
    Configure loggers with the specified format and level.

    Args:
        log_level: Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        use_basic_format: If True, use basic text format. If False, use JSON format.
        service_name: Name of the service for logging identification
        service_version: Version of the service for logging identification
    """
    # Remove default handler
    logger.remove()

    # Basic text format
    basic_format_str = " | ".join(
        [
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>",
            "<level>{level}</level>",
            "<yellow>{process}[{thread}]</yellow>",
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>",
            "<level>{message}</level>",
        ]
    )

    # Configure console handler
    if use_basic_format:
        logger.add(
            sys.stderr,
            level=log_level.upper(),
            format=basic_format_str,
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
        logger.info("Using basic logging format")
    else:
        logger.add(
            structurize_log,
            serialize=True,
            level=log_level.upper(),
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
        logger.info("Using structured logging format")

    # Set the log level for all loggers
    logger.level(log_level.upper())
    logger.info(f"Logging configured with level: {log_level}")
