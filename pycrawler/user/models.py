# -*- coding:utf-8 -*-
import logging
from pycrawler.database import CRUDMixin
from pycrawler.module import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, BadData
from flask_login import UserMixin
from flask import current_app
from pycrawler.template_filter import format_date
import logging

logger = logging.getLogger(__name__)

class Department:
    ADMINISTRATION = 0b00000000001
    MANAGEMENT     = 0b00000000010
    DEVELOPMENT    = 0b00000000100
    PRODUCTION     = 0b00000001000
    QUALITY        = 0b00000010000
    PURCHASING     = 0b00000100000
    MARKETING      = 0b00001000000

class Permission:
    USER_MANAGEMENT = 0b00000001
    ADMINISTRATOR   = 0b11111111


class User(db.Model, UserMixin, CRUDMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    department = db.Column(db.Integer, default=0)
    permission = db.Column(db.Integer, default=0)

    def _get_password(self):
        """Returns the hashed password."""
        return self._password

    def _set_password(self, password):
        """Generates a password hash for the provided password."""
        if not password:
            return
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_date': format_date(self.create_date),
            'admin': self.check_permission(Permission.ADMINISTRATOR)
        }

    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false."""

        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def generate_auth_token(self, app, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    def check_department(self, department):
        return self.department is not None and (
            self.department & department
        ) == department

    def check_permission(self, permission):
        return self.permission is not None and (
            self.permission & permission
        ) == permission

    @staticmethod
    def verify_auth_token(token, app):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        # except SignatureExpired:
        #     return None # valid token, but expired
        except BadSignature:
            logger.info('BadSignature')
            return None # invalid token
        user = User.query.get(data['id'])
        return user
