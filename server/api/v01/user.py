# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from sqlalchemy import func
from server.module import db, api
from server.models.user import User, Permission
from server.module import multi_auth
from server.api import result
from sqlalchemy import asc, desc
from flask import g, jsonify, current_app, request
import logging
import datetime
import time
from flask_cors import cross_origin
from server.utils import mark_dyn_data, get_dyn_data

logger = logging.getLogger(__name__)

list_parser = reqparse.RequestParser()
list_parser.add_argument('offset')
list_parser.add_argument('limit')


class UserLogin(Resource):
    def post(self):
        json = request.get_json(force=True)
        username = json['user_name']
        password = json['password']
        user = User.query.filter_by(name=username).first()
        if not user or not user.check_password(password):
            return result.create_response(result.NAME_PASS_ERROR)
        if not user.isActive():
            return result.create_response(result.USER_NO_ACTIVE)
        token = user.generate_auth_token(app=current_app, expiration=current_app.config['TOKEN_EXPIRE'])
        expire = time.mktime(datetime.datetime.now().timetuple()) + current_app.config['TOKEN_EXPIRE']
        return result.create_response(result.OK, {
            'token': token.decode('utf-8'),
            'expire': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expire)),
            'admin': user.check_permission(Permission.ADMINISTRATOR),
            'name': user.name
        }) 

class UserList(Resource):
    decorators = [multi_auth.login_required]
    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        users = User.query.order_by(desc(User.id)).limit(limit).offset(offset)
        count = User.with_entities(func.count(User.id)).scalar()
        # count = User.query(func.count(User.id)).scalar()

        return result.create_response (result.OK, {
            'count': count,
            'users': [x.to_json() for x in users],
        })

    def post(self):
        json = request.get_json(force=True)
        username = json['user_name']
        if User.query.filter_by(name=username).scalar() is None:
            password = json['password']
            admin = json['admin']
            user = User()
            user.name = username
            user.password = password
            if admin:
                user.permission = Permission.ADMINISTRATOR
            user.save()
            return result.create_response(result.OK, user)
        return result.create_response(result.USER_EXIST)


class UserInfo(Resource):
    decorators = [multi_auth.login_required]

    def get(self, id):
        user = User.query.filter(User.id == id).first()
        if user:
            return result.create_response(result.OK, user)
        return result.create_response(result.USER_NO_EXIST)

    def put(self, id):
        user = User.query.filter(User.id == id).first()
        if not user:
            return result.create_response(result.USER_NO_EXIST)
        json = request.get_json(force=True)
        password = json['password']
        admin = json['admin']
        active = json['active']
        logger.info(json)
        if password is not None:
            user.password = password
        if admin:
            user.permission = Permission.ADMINISTRATOR
        else:
            user.permission = 0
        if active is not None:
            user.active = active
        user.save()
        return result.create_response(result.OK, user)

    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        if not user:
            return result.create_response(result.USER_NO_EXIST)
        if user.isActive():
            user.active = False
        user.save()
        return result.create_response(result.OK)

class DynData(Resource):
    decorators = [multi_auth.login_required]

    def get(self):
        user = g.current_user
        if not user:
            return result.create_response(result.USER_NO_EXIST)
        data = get_dyn_data(user.id)
        return result.create_response(result.OK, data)

    def post(self):
        user = g.current_user
        if not user:
            return result.create_response(result.USER_NO_EXIST)
        json = request.get_json(force=True)
        data = json.get('data', None)
        if not data:
            return result.create_response(result.DATA_NO_EXIST)
        mark_dyn_data(user.id, data)
        return result.create_response(result.OK)

api.add_resource(UserInfo, '/api/v01/user/<int:id>')
api.add_resource(UserLogin, '/api/v01/user/login')
api.add_resource(UserList, '/api/v01/user')
api.add_resource(DynData, '/api/v01/dyn')
