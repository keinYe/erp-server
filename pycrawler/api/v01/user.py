
from flask_restful import Resource, reqparse
from sqlalchemy import func
from pycrawler.module import db, api
from pycrawler.user.models import User
from pycrawler.module import multi_auth
from flask import g, jsonify, current_app, request
import logging
import datetime
from flask_cors import cross_origin
logger = logging.getLogger(__name__)

parser = reqparse.RequestParser()
parser.add_argument('userName', type=str)
parser.add_argument('password', type=str)


class UserApi(Resource):
    def post(self):
        args = parser.parse_args()
        username = args.get('userName')
        password = args.get('password')
        if username is None or password is None:
            return '', 400
        user = User.query.filter(User.name == username).first()
        if user is not None:
            return jsonify({
                'name':user.name,
                'password': user.password,
            })
        user = User(name=username)
        user._set_password(password=password)
        user.save()
        return jsonify({
            'username': username
        }), 200, {'Location': '/api/1'}

class Login(Resource):
    def post(self):
        json = request.get_json(force=True)
        username = json['user_name']
        password = json['password']
        user = User.query.filter_by(name=username).first()
        if not user or not user.check_password(password):
            return jsonify({
                'userName': username
            }), 400
        token = user.generate_auth_token(current_app)
        expire = (datetime.datetime.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d')
        return jsonify({
            'token': token.decode('utf-8'),
            'expire': expire,
            'status': 1
        })

class List(Resource):
    @multi_auth.login_required
    def post(self):
        json = request.get_json(force=True)
        offset = int(json['offset']) if json['offset'] else 0
        limit = int(json['limit']) if json['limit'] else 20
        users = db.session.query(User).limit(limit).offset(offset)

        return jsonify ({
            'users':[x.to_json() for x in users],
            'status': 1
        })

class Count(Resource):
    @cross_origin()
    @multi_auth.login_required
    def get(self):
        count = db.session.query(func.count(User.id)).scalar()
        logger.info(count)
        return jsonify ({
            'count': count,
            'status': 1
        })

class TokenApi(Resource):
    decorators = [multi_auth.login_required]
    # @auth.login_required
    def get(self):
        token = g.current_user.generate_auth_token(current_app)
        logger.info(token)
        return jsonify({
            'token':token.decode('utf-8')
        })

api.add_resource(UserApi, '/api/v01/user/')
api.add_resource(TokenApi, '/api/v01/user/token')
api.add_resource(Login, '/api/v01/user/login')
api.add_resource(List, '/api/v01/user/list')
api.add_resource(Count, '/api/v01/user/count')
