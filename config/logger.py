import logging
from enum import Enum

from pythonjsonlogger import jsonlogger

APP_LOGGER_NAME = "ZW_LOGGER"


class LogLevel(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


# Configure the fields to include in the JSON output. message is the main log string itself
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = jsonlogger.JsonFormatter(log_format)

# Will output to sys.out by default
handler = logging.StreamHandler()
handler.setFormatter(formatter)

app_logger = logging.getLogger(APP_LOGGER_NAME)
app_logger.addHandler(handler)
app_logger.setLevel(logging.DEBUG)


def log(message: str, log_level: LogLevel = LogLevel.INFO, exception: Exception = None):
    logger = logging.getLogger(APP_LOGGER_NAME)
    log_exception_flag = False if exception is None else True

    logger.log(log_level.value, message, exc_info=log_exception_flag)

    # improvement -> add user id and trace id in log
