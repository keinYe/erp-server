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
)
from sqlalchemy.orm import relationship
from server.models.vendor import makers


class Category(BaseModel):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 物料种类
    name = Column(String(20), unique=True, nullable=False)
    # 编码规则, 分类的第一个元件以此为基+1 作为编码
    encode_rules = Column(String(20), unique=True)

    # 一个分类可以有多种物料
    material = relationship('Material', backref='category')

    _default_fields = [
        'id',
        'name',
        'encode_rules',
    ]

    _hidden_fields = []
    _readonly_fields = []

class Manufacturer(BaseModel):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 生产商名称
    name = Column(String(50), unique=True)

    # 一个生产商可以有多种物料
    material = relationship('Material', backref='manufacturer')

    _default_fields = [
        'id',
        'name',
    ]
    _hidden_fields = []
    _readonly_fields = []


class Material(BaseModel):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 物料编号
    serial = Column(String(20), unique=True, nullable=False)
    # 生产商编码
    manu_serial = Column(String(100), unique=True, nullable=False)
    # 描述
    desc = Column(String(200), nullable=False)
    # 立创代码
    lc_code = Column(String(20), unique=True)
    # 最后一次的采购价格
    price = Column(Float)
    # 库存数量
    stock = Column(Integer, default=0)

    # 一种物料只能有一个分类
    category_id = Column(Integer, ForeignKey('category.id'))
    # 一种物料智能有一个生产商
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'))

    vendors = relationship(
        "Vendor",
        secondary=makers,
        back_populates="materials")

    _default_fields = [
        'id',
        'serial',
        'manu_serial',
        'desc',
        'lc_code',
        'stock',
    ]
    _hidden_fields = []
    _readonly_fields = []


    def stock_add(self, quantity):
        self.stock = self.stock + quantity
        return self.stock
    
    def stock_sub(self, quantity):
        if (quantity > self.stock):
            return -1
        self.stock = self.stock - quantity
        return self.stock

