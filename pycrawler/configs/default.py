# -*- coding:utf-8 -*-

import os
import sys
import datetime

class DefaultConfig(object):
    basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                               os.path.dirname(__file__)))))

    DEBUG=True
    TESTING=False

    py_version = '{0.major}{0.minor}'.format(sys.version_info)

    # Logging Config Path
    # see https://docs.python.org/library/logging.config.html#logging.config.fileConfig
    # for more details. Should either be None or a path to a file
    # If this is set to a path, consider setting USE_DEFAULT_LOGGING to False
    # otherwise there may be interactions between the log configuration file
    # and the default logging setting.
    #
    # If set to a file path, this should be an absolute file path
    LOG_CONF_FILE = None

    # Path to store the INFO and ERROR logs
    # If None this defaults to flaskbb/logs
    #
    # If set to a file path, this should be an absolute path
    LOG_PATH = os.path.join(basedir, 'logs')

    LOG_DEFAULT_CONF = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)-7s %(name)-25s %(message)s'
            },
            'advanced': {
                'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            }
        },

        'handlers': {
            'console': {
                'level': 'NOTSET',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'pycrawler': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_PATH, 'mdpms.log'),
                'mode': 'a',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
            },

            'infolog': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_PATH, 'info.log'),
                'mode': 'a',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
            },
            'errorlog': {
                'level': 'ERROR',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_PATH, 'error.log'),
                'mode': 'a',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
            },
        },

        'loggers': {
            'flask': {
                'handlers': ['infolog', 'errorlog'],
                'level': 'INFO',
                'propagate': True
            },
            'pycrawler': {
                'handlers': ['console', 'pycrawler'],
                'level': 'INFO',
                'propagate': True
            },
        }
    }

    # When set to True this will enable the default
    # FlaskBB logging configuration which uses the settings
    # below to determine logging
    USE_DEFAULT_LOGGING = True

    # If SEND_LOGS is set to True, the admins (see the mail configuration) will
    # recieve the error logs per email.
    SEND_LOGS = False


    #Database
    # For SQLite:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/' + \
                                  'test.sqlite'
    SQLALCHEMY_BINDS = {
        'crawler': 'sqlite:///' + basedir + '/' + 'pycrawler.sqlite'
    }

    # This option will be removed as soon as Flask-SQLAlchemy removes it.
    # At the moment it is just used to suppress the super annoying warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This will print all SQL statements
    SQLALCHEMY_ECHO = False


    SECRET_KEY = 'ijkaumadidihiihddd'
    TOKEN_EXPIRE = 60 * 60 * 24

    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=10)
