import logging
from server.database import CRUDMixin
from server.module import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, BadData
from flask_login import UserMixin
from flask import current_app
from server.template_filter import format_date
import logging

logger = logging.getLogger(__name__)


class Receipt(db.Model, CRUDMixin):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    quantity = db.Column(db.Integer, unique=True, default=0)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    inoutreceipt_id = db.Column(db.Integer, db.ForeignKey('inoutreceipt.id'))

    def to_json(self):
        return {
            'id': self.id,
            'date': format_date(self.date),
            'quantity': self.quantity,
            'name': self.product.name,
            'model': self.product.model,
            'in_out': self.inoutreceipt.in_out
        }

# 出入库单数据表
class InOutReceipt(db.Model, CRUDMixin):
    __tablename__ = 'inoutreceipt'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(20), unique=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    in_out = db.Column(db.Boolean, default=False)
    record = db.relationship('Receipt', backref='inoutreceipt')

    def to_json(self):
        return {
            'id': self.id,
            'number': self.number,
            'date': format_date(self.date),
            'in_out': self.in_out
        }

# 物料/产品数据表
class Product(db.Model, CRUDMixin):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    model = db.Column(db.String(20), unique=True)
    _quantity = db.Column(db.Integer, unique=True, default=0)

    record = db.relationship('Receipt', backref='product')

    def to_json(self):
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'model': self.model,
            'quantity': self._quantity
        }

    def increase(self, amount):
        self._quantity = self._quantity + amount
        self.save()

    def inventory(self):
        return self._quantity

    def reduce(self, amout):
        if (self._quantity < amout):
            return False
        self._quantity = self._quantity - amout
        self.save()
        return True
