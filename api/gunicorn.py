# guncorn
#accesslog = 'access.log'
#accesslog = '-'
access_log_format = '%(r)s %(f)s %(s)s %(b)s %(L)s'
#errorlog = 'error.log'
#errorlog = '-'
loglevel = 'info'
#capture_output = True
logconfig_dict = {
    #'version': 1,
    'formatters': {
        'generic': {
            'format': '%(asctime)-15s\t%(process) 6d:%(levelname)s:%(name)s: %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%z',
            'class': 'logging.Formatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': 'ext://sys.stdout'
        },
        'error_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': 'ext://sys.stderr'
        },
    },
    'loggers': {
        'gunicorn.error': {
            'level': 'INFO',
            'handlers': ['error_console'],
            'propagate': False,
            'qualname': 'gunicorn.error'
        },

        'gunicorn.access': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
            'qualname': 'gunicorn.access'
        }
    },
}


import os
bind = ['{}:{}'.format(os.environ['SERVER_HOST'], os.environ['SERVER_PORT'])]
workers = 16
threads = 4
#daemon = True
#syslog = True
#syslog_prefix = 'accounts'
