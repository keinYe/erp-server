# -*- coding:utf-8 -*-

import os
import sys


class DefaultConfig(object):
    basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                               os.path.dirname(__file__)))))

    DEBUG=True
    TESTING=False

    py_version = '{0.major}{0.minor}'.format(sys.version_info)

    #Database
    # For SQLite:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/' + \
                                  'pycrawler.sqlite'

    # This option will be removed as soon as Flask-SQLAlchemy removes it.
    # At the moment it is just used to suppress the super annoying warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This will print all SQL statements
    SQLALCHEMY_ECHO = False
