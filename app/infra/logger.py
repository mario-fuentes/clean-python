from abc import ABC


class Logger(ABC):
    def exception(self, ex: Exception, msg: str = None):
        pass
