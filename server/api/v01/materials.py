# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from sqlalchemy import asc, desc
from server.module import multi_auth, api
from flask import g, jsonify, current_app, request
import logging

logger = logging.getLogger(__name__)

class Materials(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        pass

    def post(self):
        pass


class Material(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        pass

    def post(self, id):
        pass



api.add_resource(Materials, '/api/v01/materials')
api.add_resource(Material, '/api/v01/materials/<int:id>')

