# -*- coding:utf-8 -*-
import logging
from pycrawler.database import CRUDMixin
from pycrawler.module import db
import datetime


class SalesRecord(db.Model, CRUDMixin):
    __tablename__ 'salesrecord'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
