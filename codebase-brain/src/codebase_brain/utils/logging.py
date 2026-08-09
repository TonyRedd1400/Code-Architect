"""Logging utilities."""

import logging
import sys
from typing import Optional


_default_logger: Optional[logging.Logger] = None


def setup_logging(
    level: int = logging.INFO,
    format_string: str | None = None,
    output: str = "stderr",
) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (default INFO)
        format_string: Log format (default: simple format)
        output: Output destination ("stderr", "stdout", or file path)
        
    Returns:
        Configured logger
        
    Example:
        setup_logging(level=logging.DEBUG)
        logger = get_logger()
        logger.info("Application started")
    """
    global _default_logger
    
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logger
    logger = logging.getLogger("codebase_brain")
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create handler
    if output == "stderr":
        handler = logging.StreamHandler(sys.stderr)
    elif output == "stdout":
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler(output)
    
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    _default_logger = logger
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (optional, uses default if not provided)
        
    Returns:
        Logger instance
        
    Example:
        logger = get_logger("scanner")
        logger.debug("Scanning directory %s", path)
    """
    if name is None:
        if _default_logger is None:
            setup_logging()
        return _default_logger
    
    return logging.getLogger(f"codebase_brain.{name}")


class ProgressReporter:
    """Simple progress reporter for long operations."""
    
    def __init__(self, total: int, description: str = "Processing"):
        """
        Initialize progress reporter.
        
        Args:
            total: Total number of items
            description: Description of the operation
        """
        self.total = total
        self.description = description
        self.current = 0
        self.logger = get_logger("progress")
    
    def update(self, n: int = 1) -> None:
        """
        Update progress by n items.
        
        Args:
            n: Number of items completed
        """
        self.current += n
        if self.current % max(1, self.total // 10) == 0:
            percent = min(100, (self.current / self.total) * 100)
            self.logger.info(f"{self.description}: {percent:.1f}% ({self.current}/{self.total})")
    
    def finish(self) -> None:
        """Mark operation as complete."""
        self.logger.info(f"{self.description}: Complete ({self.total} items)")
