# -*- coding:utf-8 -*-
import logging
from pycrawler.database import CRUDMixin
from pycrawler.module import db
import datetime



class Contact(db.Model, CRUDMixin):
    ''' 联系人 '''
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    tel = db.Column(db.String(20))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))

    # sales_record = db.relationship('SalesRecord', backref='contact')


class Agent(db.Model, CRUDMixin):
    ''' 代理商 '''
    __tablename__ = 'agent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    tel = db.Column(db.String(20))
    fax = db.Column(db.String(20))
    contact = db.relationship('Contact', backref='agent')
    # sales_record = db.relationship('SalesRecord', backref='agent')
