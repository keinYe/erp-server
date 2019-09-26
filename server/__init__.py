# -*- coding:utf-8 -*-

__version__ = '0.0.1'
import logging
from server.app import create_app
from server.api.v01 import user #noqa

logger = logging.getLogger(__name__)
