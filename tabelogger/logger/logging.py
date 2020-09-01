from abc import ABCMeta, abstractmethod


class Logging:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_logger(self, name: str):
        pass
