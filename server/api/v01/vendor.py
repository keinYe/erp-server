# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from sqlalchemy import asc, desc
from server.module import multi_auth, api
from server.models.vendor import (
    Vendor,
    Liaison
)
from sqlalchemy import asc, desc, func
from flask import g, jsonify, current_app, request
from server.api import result
import logging


class LiaisonList(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        liaisons = Liaison.query.order_by(desc(Liaison.id)).limit(limit).offset(offset)
        count = Liaison.query.with_entities(func.count(Liaison.id)).scalar()
        return result.create_response(result.OK, {
            'count': count,
            'liaison': [x.to_dict() for x in liaisons]
        })

    def post(self):
        json = request.get_json(force=True)
        name = json.get('name', None)
        if name is None:
            return result.create_response(result.DATA_NO_EXIST)
        liaison = Liaison.query.filter_by(name=name).first()
        if liaison:
            return result.create_response(result.DATA_IS_EXIST)
        liaison = Liaison()
        liaison.name = name
        liaison.tel = json.get('tel', None)
        liaison.qq = json.get('qq', None)
        vendor_id = json.get('vendor_id', None)
        if vendor_id is not None:
            vendor = Vendor.query.filter_by(id=vendor_id).first()
            if vendor is None:
                return result.create_response(result.DATA_NO_EXIST)
            liaison.vendor = vendor
        liaison.save()
        return result.create_response(result.OK, liaison)   

class LiaisonInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        liaison = Liaison.query.filter_by(id=id).first()
        if liaison is None:
            return result.create_response(result.ID_NOT_EXIST)
        return result.create_response(result.OK, liaison)

    def put(self, id):
        liaison = Liaison.query.filter_by(id=id).first()
        if liaison is None:
            return result.create_response(result.ID_NOT_EXIST)   
        json = request.get_json(force=True)
        if json.get('name', None):
            liaison.name = json.get('name')
        if json.get('tel', None):
            liaison.tel = json.get('tel')
        if json.get('qq', None):
            liaison.qq = json.get('qq')
        vendor_id = json.get('vendor_id', None)
        if vendor_id is not None:
            vendor = Vendor.query.filter_by(id=vendor_id).first()
            if vendor is None:
                return result.create_response(result.DATA_NO_EXIST)
            liaison.vendor = vendor
        liaison.save()
        return result.create_response(result.OK, liaison)      

class VendorList(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        vendors = Vendor.query.order_by(desc(Vendor.id)).limit(limit).offset(offset)
        count = Vendor.query.with_entities(func.count(Vendor.id)).scalar()
        return result.create_response(result.OK, {
            'count': count,
            'liaison': [x.to_dict() for x in vendors]
        })

    def post(self):
        json = request.get_json(force=True)
        name = json.get('name', None)
        if name is None:
            return result.create_response(result.DATA_NO_EXIST)
        vendor = Vendor.query.filter_by(name=name).first()
        if vendor is not None:
            return result.create_response(result.DATA_IS_EXIST)
        vendor = Vendor()
        vendor.address = json.get('address', None)
        vendor.tax_number = json.get('tax_number', None)
        lialison_id = json.get('liaison_id', None)
        if lialison_id:
            liaison = Liaison.query.filter_by(id=lialison_id).first()
            if liaison is None:
                return result.create_response(result.DATA_NO_EXIST)
            vendor.liaison.append(liaison)
        vendor.save()
        return result.create_response(result.OK, vendor)
        
class VendorInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        pass

    def put(self, id):
        pass

api.add_resource(LiaisonList, '/api/v01/liaison')
api.add_resource(LiaisonInfo, '/api/v01/liaison/<int:id>')
api.add_resource(VendorList, '/api/v01/vendor')
api.add_resource(VendorInfo, '/api/v01/vendor/<int:id>')