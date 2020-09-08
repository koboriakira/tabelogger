from tabelogger.logger.logging import Logging
from fastapi.logger import logger as fastapi_logger
from tabelogger.logger.logging import Logging


class FastapiLogging(Logging):

    def get_logger(self, name: str):
        return fastapi_logger
