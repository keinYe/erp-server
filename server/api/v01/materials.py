# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from sqlalchemy import asc, desc
from server.module import multi_auth, api
from server.models.materials import (
    Material,
    Manufacturer,
    Category,
)
from sqlalchemy import asc, desc, func
from flask import g, jsonify, current_app, request
from server.api import result
import logging

logger = logging.getLogger(__name__)

class Categorys(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        categorys = Category.query.order_by(desc(Category.id)).limit(limit).offset(offset)
        count = Category.query.with_entities(func.count(Category.id)).scalar()
        return result.create_response(result.OK, {
            'count': count,
            'category': [x.to_dict() for x in categorys]
        })

    def post(self):
        json = request.get_json(force=True)
        name = json.get('name', None)
        if name is None:
            return result.create_response(result.DATA_NO_EXIST)
        category = Category()
        category.name = name
        category.save()
        return result.create_response(result.OK, category)       

class CategoryInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        category = Category.query.filter_by(id=id).first()
        if category is None:
            return result.create_response(result.ID_NOT_EXIST)
        return result.create_response(result.OK, category)

    def post(self, id):
        category = Category.query.filter_by(id=id).first()
        if category is None:
            return result.create_response(result.ID_NOT_EXIST)   
        json = request.get_json(force=True)
        name = json.get('name', None)
        if name is None:
            return result.create_response(result.DATA_NO_EXIST)
        category.name = name
        category.save()
        return result.create_response(result.OK, category)                    


class Manufacturers(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        manufactures = Manufacturer.query.order_by(desc(Manufacturer.id)).limit(limit).offset(offset)
        count = Manufacturer.query.with_entities(func.count(Manufacturer.id)).scalar()
        return result.create_response(result.OK, {
            'count': count,
            'manufacturer': [x.to_dict() for x in manufactures]
        })

    def post(self):
        json = request.get_json(force=True)
        name = json.get('name', None)
        if name is None:
            return result.create_response(result.DATA_NO_EXIST)
        manufacturer = Manufacturer()
        manufacturer.name = name
        manufacturer.save()
        return result.create_response(result.OK, manufacturer)

class ManufacturerInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        manufacturer = Manufacturer.query.filter_by(id=id).first()
        if not manufacturer:
            return result.create_response(result.ID_NOT_EXIST)
        return result.create_response(result.OK, manufacturer)

    def post(self, id):
        manufacturer = Manufacturer.query.filter_by(id=id).first()
        if not manufacturer:
            return result.create_response(result.ID_NOT_EXIST)
        json = request.get_json(force=True)
        name = json.get('name', None)
        if name is None:
            return result.create_response(result.DATA_NO_EXIST)
        manufacturer.name = name
        manufacturer.save()
        return result.create_response(result.OK, manufacturer)


class Materials(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        materials = Material.order_by(desc(Material.id)).limit(limit).offset(offset)
        count = Material.query.with_entities(func.count(Material.id)).scalar()
        return result.create_response(result.OK, {
            'count': count,
            'materials': [x.to_dict() for x in materials]
        })

    def post(self):
        json = request.get_json(force=True)
        serial = json.get('serial', None)
        manu_serial = json.get('manu_serial', None)
        desc = json.get('desc', None)
        category_id = json.get('category_id', None)
        manufacturer_id = json.get('manufacturer_id', None)
        if not serial or not manu_serial or not desc or not category_id or not manufacturer_id:
            return result.create_response(result.DATA_NO_EXIST)
        category = Category.query.filter_by(id=category_id).first()
        manufacturer = Manufacturer.query.filter_by(id=manufacturer_id).first()
        if not category or not manufacturer:
            return result.create_response(result.DATA_NO_EXIST)
        material = Material()
        material.serial = serial
        material.manu_serial = manu_serial
        material.desc = desc
        material.category = category
        material.manufacturer = manufacturer
        material.save()
        return result.create_response(result.OK, material)

class MaterialInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        material = Material.query.filter_by(id=id).first()
        if not material:
            return result.create_response(result.ID_NOT_EXIST)
        return result.create_response(result.OK, material)

    def post(self, id):
        material = Material.query.filter_by(id=id).first()
        if not material:
            return result.create_response(result.ID_NOT_EXIST)
        json = request.get_json(force=True)
        material.serial = json.get('serial') if json.get('serial', None) else material.serial
        material.manu_serial = json.get('manu_serial') if json.get('manu_serial', None) else material.manu_serial
        material.desc = json.get('desc') if json.get('desc', None) else material.desc
        category_id = json.get('category_id', None)
        manufacturer_id = json.get('manufacturer_id', None)
        category = Category.query.order_by(id=category_id).first()
        manufacturer = Manufacturer.query.order_by(id=manufacturer_id).first()
        if category:
            material.category = category
        if manufacturer:
            material.manufacturer = manufacturer
        manufacturer.save()     
        return result.create_response(result.OK, material)


api.add_resource(Categorys, '/api/v01/categorys')
api.add_resource(CategoryInfo, '/api/v01/categorys/<int:id>')
api.add_resource(Manufacturers, '/api/v01/manufactrures')
api.add_resource(ManufacturerInfo, '/api/v01/manufactrures/<int:id>')
api.add_resource(Materials, '/api/v01/materials')
api.add_resource(MaterialInfo, '/api/v01/materials/<int:id>')


