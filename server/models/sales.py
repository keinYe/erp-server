# -*- coding:utf-8 -*-
import logging
from server.database import CRUDMixin
from server.module import db
import datetime
# from pycrawler.agent.models import Agent, Contact

class Agent(db.Model, CRUDMixin):
    ''' 代理商 '''
    __tablename__ = 'agent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(200), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    tel = db.Column(db.String(20))
    fax = db.Column(db.String(20))
    contact = db.relationship('Contact', backref='agent')
    salesrecord = db.relationship('SalesRecord', backref='agent')

class Contact(db.Model, CRUDMixin):
    ''' 联系人 '''
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(200), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    tel = db.Column(db.String(20))

    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    salesrecord = db.relationship('SalesRecord', backref='contact')

class SalesRecord(db.Model, CRUDMixin):
    __tablename__ = 'salesrecord'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nmuber = db.Column(db.String(20), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    model = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    applicant = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.String(200))

    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
