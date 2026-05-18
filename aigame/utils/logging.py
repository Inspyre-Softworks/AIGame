'''Logging utilities with optional InspyLogger integration.

Taylor B. | Inspyre-Softworks
'''

import logging


def _create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
    return logger


class Loggable:
    '''Mixin that exposes a module-specific logger.'''

    @property
    def logger(self) -> logging.Logger:
        return _create_logger(self.__class__.__name__)
