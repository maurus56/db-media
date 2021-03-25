# import logging

logging_config = {
    'version': 1,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-10s %(processName)-10s : %(message)s'
        },
        'simple': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-10s %(levelname)-8s : %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/info.log',
            'mode': 'a',
            'level': 'INFO',
            'formatter': 'simple',
        },
        'errors': {
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
            'mode': 'a',
            'level': 'ERROR',
            'formatter': 'simple',
        },
    },
    'MyScrapper': {
        'handlers': ['console', 'file']
    },
    'db_actions': {
        'handlers': ['console', 'file']
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file', 'errors']
    },
}