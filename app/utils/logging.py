import logging
import json
from typing import Any, Dict, Optional


class StructuredFormatter(logging.Formatter):
    """JSON-based structured logging formatter."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields if present
        if hasattr(record, "session_id"):
            log_data["session_id"] = record.session_id
        if hasattr(record, "state"):
            log_data["state"] = record.state
        if hasattr(record, "extra_data"):
            log_data["data"] = record.extra_data
            
        return json.dumps(log_data)


def get_logger(name: str, structured: bool = False) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Prevent duplicate handlers

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    
    if structured:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def log_with_context(
    logger: logging.Logger,
    level: int,
    message: str,
    session_id: Optional[str] = None,
    state: Optional[str] = None,
    extra_data: Optional[Dict[str, Any]] = None,
) -> None:
    """Log a message with optional structured context."""
    extra = {}
    if session_id:
        extra["session_id"] = session_id
    if state:
        extra["state"] = state
    if extra_data:
        extra["extra_data"] = extra_data
    
    logger.log(level, message, extra=extra)
