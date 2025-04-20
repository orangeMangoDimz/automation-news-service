from pathlib import Path
from dotenv import load_dotenv
from pydantic import ValidationError
from utils.constant import API_KEY_NOT_FOUND, DEBUG_MODE, ENV_NOT_COMPLETE
from typing import List
from utils.type_hint import EnvType
from logging.handlers import RotatingFileHandler
from typing import Optional
import logging
import os


class LoadSettings:
    """
    LoadSettings is a utility class for managing environment variables.
    """

    @staticmethod
    def get_env() -> List[EnvType]:
        dotenv_path = Path(".env")
        load_dotenv(dotenv_path=dotenv_path)

        list_env: List[EnvType] = [
            {
                "key": "GEMINI_API_KEY",
                "value": "",
                "err_msg": API_KEY_NOT_FOUND,
            },
            {
                "key": "DEBUG_MODE",
                "value": "",
                "err_msg": DEBUG_MODE,
            },
        ]

        for env in list_env:
            key = env.get("key")
            if key is None:
                raise ValidationError(ENV_NOT_COMPLETE)

            value: str | None = os.getenv(key)
            if key == "DEBUG_MODE" and value is None:
                value = "True"
                print(env.get("err_msg"))
            elif value is None:
                raise ValidationError(env.get("err_msg"))

            env["value"] = value

        return list_env


class AppLogger:
    """
    A modular logger class that provides flexible logging configuration.
    """

    def __init__(
        self,
        name: Optional[str] = __name__,
        log_level: int = logging.INFO,
        log_file: Optional[str] = None,
        max_bytes: int = 1000000,
        backup_count: int = 5,
        fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ):

        # Use the provided name or default to the class name
        logger_name = name or self.__class__.__name__
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.formatter = logging.Formatter(fmt)

        # Remove any existing handlers to avoid duplicate logs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Always add console handler
        self._add_console_handler()

        # Add file handler if log file specified
        if log_file:
            self._add_file_handler(log_file, max_bytes, backup_count)

    def _add_console_handler(self) -> None:
        """
        Add a stream handler for console output
        """
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(
        self, log_file: str, max_bytes: int, backup_count: int
    ) -> None:
        """
        Add a rotating file handler for file logging
        """
        file_handler = RotatingFileHandler(
            filename=log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        """
        Log a debug message
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """
        Log an info message
        """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """
        Log a warning message
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """
        Log an error message
        """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """
        Log a critical message
        """
        self.logger.critical(message)

    def exception(self, message: str) -> None:
        """
        Log an exception message with traceback.
        Should be called within an except block.
        """
        self.logger.exception(message)

    def set_level(self, level: int) -> None:
        """
        Set the logging level for all handlers
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
