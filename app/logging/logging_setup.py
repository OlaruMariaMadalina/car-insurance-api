import logging, sys, structlog, os

def setup_logging():
    """
    Configures logging for the application using structlog and the standard logging module.

    - Sets the log level from the LOG_LEVEL environment variable (default: INFO).
    - Logs to stdout with a simple message format.
    - Adds processors for log level, timestamp, and exception formatting.
    - Uses ConsoleRenderer for human-readable output.
    - Sets APScheduler and SQLAlchemy engine logs to WARNING to reduce noise.
    """
    level =  os.getenv("LOG_LEVEL", "INFO").upper()
    
    logging.basicConfig(level=level, stream=sys.stdout, format="%(message)s")
    
    processors_common = [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
    ]
    
    processors = [*processors_common, structlog.dev.ConsoleRenderer()]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level, logging.INFO)),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)