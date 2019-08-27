# -*- coding:utf-8 -*-

__version__ = '0.0.1'
import logging
from pycrawler.app import create_app
from pycrawler.api.v01 import crawler, user #noqa
from pluggy import HookimplMarker

impl = HookimplMarker('pycrawler')

logger = logging.getLogger(__name__)
