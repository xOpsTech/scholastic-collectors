__author__ = 'evantha'

import logging.config
import os

TRACE = 15
logging.addLevelName(TRACE, 'TRACE')


def log_trace(self, msg, *args, **kwargs):
    self.log(TRACE, msg, *args, **kwargs)


logging.Logger.trace = log_trace
logging.TRACE = TRACE

info_log_file = os.path.join(os.path.dirname(__file__), 'info.log')
error_log_file = os.path.join(os.path.dirname(__file__), 'error.log')

FORMAT = '%(levelname)s - %(asctime)s - %(name)s - %(funcName)s | %(message)s'

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {'format': FORMAT}
    },
    'handlers': {
        'info_log_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': info_log_file,
            'formatter': 'standard',
            'level': os.getenv('SCHOLASTIC_LOG_LEVEL', 'INFO'),
            'when': 'midnight',
            'encoding': 'utf8'
        },
        'error_log_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': error_log_file,
            'formatter': 'standard',
            'level': logging.ERROR,
            'when': 'midnight',
            'encoding': 'utf8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['info_log_file', 'error_log_file'],
            'level': logging.DEBUG
        }
    }
}
logging.config.dictConfig(LOG_CONFIG)
