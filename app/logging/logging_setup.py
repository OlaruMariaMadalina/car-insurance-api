import logging, sys, structlog, os

def setup_logging():
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