from settings import AppLogger


class LoggerMixin:
    def __init_logger__(self):
        self.logger = AppLogger(name=self.__class__.__name__).logger
