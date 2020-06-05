# -*- coding:utf-8 -*-
import logging
from server.module import db
from server.database import BaseModel
import datetime
from server.template_filter import format_date
from sqlalchemy import (
    Integer,
    Column,
    String,
    ForeignKey,
    Float,
    Table,
)
from sqlalchemy.orm import relationship

makers = Table('makers', db.metadata,
    Column('material_id', Integer, ForeignKey('materials.id')),
    Column('vendor_id', Integer, ForeignKey('vendor.id'))
)

class Liaison(BaseModel):
    __tablename__ = 'liaison'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 名称
    name = Column(String(20), unique=True, nullable=False)
    # 电话
    tel = Column(String(20))
    # QQ
    qq = Column(String(20))

    vendor_id = Column(Integer, ForeignKey('vendor.id'))

    _default_fields = [
        'id',
        'number',
        'tel',
        'qq',
    ]


class Vendor(BaseModel):
    __tablename__ = 'vendor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 名称
    name = Column(String(20), unique=True, nullable=False)
    # 地址
    address = Column(String(200))
    # 税号
    tax_number = Column(String(100))

    liaison = relationship('Liaison', backref='vendor')

    materials = relationship(
        "Material",
        secondary=makers,
        back_populates="vendors")

    _default_fields = [
        'id',
        'name',
        'address',
        'tax_number',
    ]
    _hidden_fields = []
    _readonly_fields = []
