# -*- coding:utf-8 -*-
import logging
from pycrawler.database import CRUDMixin
from pycrawler.module import db
import datetime



class Contact(db.Model, CRUDMixin):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    tel = db.Column(db.String(20))
    # sales_record = db.relationship('SalesRecord', backref='contact')


class Agent(db.Model, CRUDMixin):
    __tablename__ = 'agent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    tel = db.Column(db.String(20))
    fax = db.Column(db.String(20))

    # sales_record = db.relationship('SalesRecord', backref='agent')
