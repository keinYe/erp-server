# -*- coding:utf-8 -*-

import logging
from pycrawler.database import CRUDMixin
from pycrawler.module import db
import datetime


class Brands(db.Model, CRUDMixin):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    url = db.Column(db.String(100))
    desc = db.Column(db.Text)
    materials = db.relationship('Materials', backref='brands')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'desc': self.desc,
        }

class Materials(db.Model, CRUDMixin):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), unique=True, nullable=False)
    package = db.Column(db.String(50), nullable=False)
    price = db.relationship('Price', backref='materials')
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'catalog': self.catalog.name,
            'model': self.model,
            'number': self.number,
            'package': self.package,
            'brand': self.brands.name,
            'price': [x.to_json() for x in self.price],
        }

class Price(db.Model, CRUDMixin):
    __tablename__ = 'price'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    price = db.Column(db.Text)
    materials_id = db.Column(db.Integer, db.ForeignKey('materials.id'))

    def to_json(self):
        return {
            'date':self.date,
            'price':self.price,
        }

class Catalog(db.Model, CRUDMixin):
    __tablename__ = 'catalog'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("catalog.id"))
    parent = db.relationship("Catalog", remote_side=[id], backref='catalog')
    materials = db.relationship('Materials', backref='catalog')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_name': None if not self.parent else self.parent.name,
            'parent_id': None if not self.parent else self.parent.id,
            'child': [{'name':x.name, 'id':x.id} for x in self.catalog]
        }
