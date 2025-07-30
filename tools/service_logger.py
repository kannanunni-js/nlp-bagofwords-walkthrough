# ruff: noqa: W291
"""
Service logger
"""

import logging
import sys

from loguru import logger
import shutil


class InterceptHandler(logging.Handler):
    """
    Custom logging handler for intercepting log records.

    This class is a subclass of `logging.Handler` that intercepts log records and
    logs them using a different logging system. It ensures the appropriate log
    level and additional context like call depth and exception information are
    properly handled during logging.

    :ivar name: The name of the handler.
    :type name: str
    :ivar level: The log level of the handler.
    :type level: int
    """

    def emit(self, record):  # pragma: no cover
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# Replace all handlers with the intercept
def init_logger(log_level: str):
    """
    Configures and initializes the logger for the application with a custom logging format.
    Allows for colored output, log level specification, and manages verbosity for specific loggers.

    :param log_level: Logging level to set for the application. It can be DEBUG, INFO, WARNING, ERROR, or CRITICAL.
    :type log_level: str
    :return: None
    """
    custom_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level.icon} <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level.upper(),
        format=custom_format,
        serialize=False,
        colorize=True,
    )

    logger.propagate = False
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=log_level.upper(),
    )

    # default uvicorn logger is too verbose
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("pytest").setLevel(logging.DEBUG)

    ascii_art = """
    ██╗  ██╗     █████╗     ███╗   ██╗    ███╗   ██╗     █████╗     ███╗   ██╗    ██╗   ██╗    ███╗   ██╗    ███╗   ██╗    ██╗
    ██║ ██╔╝    ██╔══██╗    ████╗  ██║    ████╗  ██║    ██╔══██╗    ████╗  ██║    ██║   ██║    ████╗  ██║    ████╗  ██║    ██║
    █████╔╝     ███████║    ██╔██╗ ██║    ██╔██╗ ██║    ███████║    ██╔██╗ ██║    ██║   ██║    ██╔██╗ ██║    ██╔██╗ ██║    ██║
    ██╔═██╗     ██╔══██║    ██║╚██╗██║    ██║╚██╗██║    ██╔══██║    ██║╚██╗██║    ██║   ██║    ██║╚██╗██║    ██║╚██╗██║    ██║
    ██║  ██╗    ██║  ██║    ██║ ╚████║    ██║ ╚████║    ██║  ██║    ██║ ╚████║    ╚██████╔╝    ██║ ╚████║    ██║ ╚████║    ██║
    ╚═╝  ╚═╝    ╚═╝  ╚═╝    ╚═╝  ╚═══╝    ╚═╝  ╚═══╝    ╚═╝  ╚═╝    ╚═╝  ╚═══╝     ╚═════╝     ╚═╝  ╚═══╝    ╚═╝  ╚═══╝    ╚═╝
    """

    terminal_width = shutil.get_terminal_size((80, 20)).columns

    # Center each line individually
    centered_art = "\n".join(line.center(terminal_width) for line in ascii_art.strip("\n").split("\n"))

    logger.info(f"\n{centered_art}")