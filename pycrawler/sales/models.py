# -*- coding:utf-8 -*-
import logging
from pycrawler.database import CRUDMixin
from pycrawler.module import db
import datetime
from pycrawler.agent.models import Agent, Contact


class SalesRecord(db.Model, CRUDMixin):
    __tablename__ = 'salesrecord'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    device_model = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    applicant = db.Column(db.String(50), nullable=False)
    agent = db.Column(db.String(200))
    contact = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    tel = db.Column(db.String(20))
    remarks = db.Column(db.String(200))
