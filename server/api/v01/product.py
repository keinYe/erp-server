# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from sqlalchemy import func, asc, desc
from server.module import db, api, multi_auth
from server.models.sales import SalesRecord, Agent, Contact
from server.models.products import Product, Receipt, InOutReceipt
from flask import g, jsonify, current_app, request
import logging
import datetime
import time

logger = logging.getLogger(__name__)

# 单个物料/产品信息获取、变更
class RroductInfo(Resource):
    decorators = [multi_auth.login_required]
    def get(self, id):
        product = Product.query.filter(Product.id == id).first()
        if product:
            return jsonify({
                'status': 1,
                'user': product.to_json()
            })
        return jsonify({
            'status': 0,
            'message': "物料 id = " + id + "不存在！"
        })

    def put(self, id):
        product = Product.query.filter(Product.id == id).first()
        if not product:
            return jsonify({
                'status': 0,
                'message': "物料 id = " + id + "不存在！"
            })
        return jsonify({
            'status': 1,
            'message': "物料 id = " + id + "更新完成！"
        })

# 物料/产品列表  新增物料/产品
class ProductList(Resource):
    decorators = [multi_auth.login_required]
    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        products = db.session.query(Product).order_by(desc(Product.id)).limit(limit).offset(offset)
        count = db.session.query(func.count(Product.id)).scalar()

        return jsonify ({
            'count': count,
            'products': [x.to_json() for x in products],
            'status': 1
        })

    def post(self):
        json = request.get_json(force=True)
        number = json['number']
        if Product.query.filter_by(number==number).scalar():
            return jsonify({
                'status': 0,
                'message': "编号: " + number + " 已存在！"
            })
        name = json['name']
        if Product.query.filter_by(name==name).scalar():
            return jsonify({
                'status': 0,
                'message': "名称: " + name + " 已存在！"
            })
        model = json['model']
        if Product.query.filter_by(model==model).scalar():
            return jsonify({
                'status': 0,
                'message': "型号: " + model + " 已存在！"
            })

        product = Product()
        product.number = number
        product.name = name
        product.model = model
        product.save()

        return jsonify({
            'status': 1
        })
