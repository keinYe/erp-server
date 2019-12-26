# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from sqlalchemy import func
from server.module import db, api
from server.models.user import User, Permission
from server.module import multi_auth
from sqlalchemy import asc, desc
from flask import g, jsonify, current_app, request
import logging
import datetime
import time
from flask_cors import cross_origin
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
            return jsonify({
                'status': 0,
                'message': '用户名或密码错误！'
            })
        if not user.isActive():
            return jsonify({
                'status': 0,
                'message': '用户未激活，请与管理员联系！'
            })
        token = user.generate_auth_token(app=current_app, expiration=current_app.config['TOKEN_EXPIRE'])
        expire = time.mktime(datetime.datetime.now().timetuple()) + current_app.config['TOKEN_EXPIRE']
        return jsonify({
            'token': token.decode('utf-8'),
            'expire': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expire)),
            'admin': user.check_permission(Permission.ADMINISTRATOR),
            'name': user.name,
            'status': 1
        })

class UserList(Resource):
    decorators = [multi_auth.login_required]
    def get(self):
        offset = int(request.args['offset']) if request.args['offset'] else 0
        limit = int(request.args['limit']) if request.args['limit'] else 20
        users = db.session.query(User).order_by(desc(User.id)).limit(limit).offset(offset)
        count = db.session.query(func.count(User.id)).scalar()

        return jsonify ({
            'count': count,
            'users': [x.to_json() for x in users],
            'status': 1
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
            return jsonify({
                'status': 1
            })
        return jsonify({
            'status': 0,
            'message': "用户名: " + username + " 已存在！"
        })


class UserInfo(Resource):
    decorators = [multi_auth.login_required]
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        if user:
            return jsonify({
                'status': 1,
                'user': user.to_json()
            })
        return jsonify({
            'status': 0,
            'message': "用户 id = " + id + "不存在！"
        })
    def put(self, id):
        user = User.query.filter(User.id == id).first()
        if not user:
            return jsonify({
                'status': 0,
                'message': "用户 id = " + str(id) + "不存在！"
            })
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
        return jsonify({
            'status': 1,
            'message': "用户 id = " + str(id) + "更新完成！"
        })

    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        if not user:
            return jsonify({
                'status': 0,
                'message': "用户 id = " + str(id) + "不存在！"
            })
        if user.isActive():
            user.active = False
        user.save()
        return jsonify({
            'status': 1,
            'message': "用户 id = " + str(id) + "已删除！"
        })


api.add_resource(UserInfo, '/api/v01/user/<int:id>')
api.add_resource(UserLogin, '/api/v01/user/login')
api.add_resource(UserList, '/api/v01/user')
