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
from server.module import db

logger = logging.getLogger(__name__)

class Categorys(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        categorys = Category.query.order_by(desc(Category.id)).limit(limit).offset(offset)
        count = Category.query.with_entities(func.count(Category.id)).scalar()
        category_list = []
        for category in categorys:
            number = Material.query.with_entities(func.count(Material.id)) \
                    .filter_by(category_id=Category.id).scalar()
            data = {
                'id' : category.id,
                'name' : category.name,
                'encode_rules' : category.encode_rules,
                'material_count' : number
            }
            category_list.append(data)
        return result.create_response(result.OK, {
            'count': count,
            'category': category_list
        })

    def post(self):
        json = request.get_json(force=True)
        name = json.get('name', None)
        encode_rules = json.get('encode_rules', None)
        if name is None or encode_rules is None:
            return result.create_response(result.DATA_NO_EXIST)
        category = Category.query.filter_by(name=name).first()
        if category:
            return result.create_response(result.DATA_IS_EXIST)
        category = Category()
        category.name = name
        category.encode_rules = encode_rules
        category.save()
        return result.create_response(result.OK, category)       

class CategoryInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        category = Category.query.filter_by(id=id).first()
        if category is None:
            return result.create_response(result.ID_NOT_EXIST)
        return result.create_response(result.OK, category)

    def put(self, id):
        category = Category.query.filter_by(id=id).first()
        if category is None:
            return result.create_response(result.ID_NOT_EXIST)   
        json = request.get_json(force=True)
        name = json.get('name', None)
        if name:
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
        manufacturer = Manufacturer.query.filter_by(name=name).first()
        if manufacturer:
            return result.create_response(result.DATA_IS_EXIST)
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

    def put(self, id):
        manufacturer = Manufacturer.query.filter_by(id=id).first()
        if not manufacturer:
            return result.create_response(result.ID_NOT_EXIST)
        json = request.get_json(force=True)
        name = json.get('name', None)
        if name:
            manufacturer.name = name
        manufacturer.save()
        return result.create_response(result.OK, manufacturer)


class Materials(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        materials = Material.query.order_by(desc(Material.id)).limit(limit).offset(offset)
        count = Material.query.with_entities(func.count(Material.id)).scalar()
        return result.create_response(result.OK, {
            'count': count,
            'materials': [x.to_dict() for x in materials]
        })

    def post(self):
        json = request.get_json(force=True)
        manu_serial = json.get('manu_serial', None)
        description = json.get('desc', None)
        category_id = json.get('category_id', None)
        manufacturer_id = json.get('manufacturer_id', None)
        if not manu_serial or not desc or not category_id or not manufacturer_id:
            return result.create_response(result.DATA_NO_EXIST)
        category = Category.query.filter_by(id=category_id).first()
        manufacturer = Manufacturer.query.filter_by(id=manufacturer_id).first()
        if not category or not manufacturer:
            return result.create_response(result.DATA_NO_EXIST)

        material = Material.query.filter_by(manu_serial=manu_serial).first()
        if material:
            return result.create_response(result.DATA_IS_EXIST)
        serial = ''
        tmp = Material.query.filter_by(category_id=category.id).order_by(desc(Material.serial)).first()
        if not tmp:
            serial = str(int(category.encode_rules) + 1)
        else:
            serial = str(int(tmp.serial) + 1)
        material = Material()
        material.serial = serial
        material.manu_serial = manu_serial
        material.desc = description
        material.category = category
        material.manufacturer = manufacturer
        material.lc_code = json.get('lc_code')
        material.save()
        return result.create_response(result.OK, material)

class MaterialInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        material = Material.query.filter_by(id=id).first()
        if not material:
            return result.create_response(result.ID_NOT_EXIST)
        return result.create_response(result.OK, material)

    def put(self, id):
        material = Material.query.filter_by(id=id).first()
        if not material:
            return result.create_response(result.ID_NOT_EXIST)
        json = request.get_json(force=True)
        material.serial = json.get('serial') if json.get('serial', None) else material.serial
        material.manu_serial = json.get('manu_serial') if json.get('manu_serial', None) else material.manu_serial
        material.desc = json.get('desc') if json.get('desc', None) else material.desc
        material.lc_code = json.get('lc_code') if json.get('lc_code') else material.lc_code
        category_id = json.get('category_id', None)
        manufacturer_id = json.get('manufacturer_id', None)
        category = Category.query.filter_by(id=category_id).first()
        manufacturer = Manufacturer.query.filter_by(id=manufacturer_id).first()
        if category:
            material.category = category
        if manufacturer:
            material.manufacturer = manufacturer
        material.save()
        return result.create_response(result.OK, material)


api.add_resource(Categorys, '/api/v01/categorys')
api.add_resource(CategoryInfo, '/api/v01/categorys/<int:id>')
api.add_resource(Manufacturers, '/api/v01/manufacturer')
api.add_resource(ManufacturerInfo, '/api/v01/manufacturer/<int:id>')
api.add_resource(Materials, '/api/v01/materials')
api.add_resource(MaterialInfo, '/api/v01/materials/<int:id>')


