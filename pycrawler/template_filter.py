# -*- coding:utf-8 -*-

# from pytz import UTC, timezone
from datetime import datetime, timedelta, timezone
import logging
import pytz

logger = logging.getLogger(__name__)

def format_date(date):
    return (date + timedelta(hours=8)).strftime('%Y-%m-%d')
    # return date.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
    # return date.astimezone(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
