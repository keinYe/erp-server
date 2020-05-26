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

class Materials(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        materials = Material.order_by(desc(Material.id)).limit(limit).offset(offset)
        count = Material.with_entities(func.count(Material.id)).scalar
        return result.create_response(result.OK, {
            'count': count,
            'materials': [x.to_dict() for x in materials]
        })

    def post(self):
        pass


class MaterialInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        material = Material.query.filter_by(id=id).one()
        if not material:
            return result.create_response(result.UNKNOWN)
        return result.create_response(result.OK, material)

    def post(self, id):
        material = Material.query.filter_by(id=id).one()
        if not material:
            return result.create_response(result.UNKNOWN)
        
        return result.create_response(result.OK, material)



api.add_resource(Materials, '/api/v01/materials')
api.add_resource(MaterialInfo, '/api/v01/materials/<int:id>')

