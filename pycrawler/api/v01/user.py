
from flask_restful import Resource, reqparse
from sqlalchemy import func
from pycrawler.module import db, api
from pycrawler.user.models import User
from pycrawler.module import auth
from flask import g, jsonify, current_app


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)


class UserApi(Resource):
    def post(self):
        args = parser.parse_args()
        username = args.get('username')
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

class TokenApi(Resource):
    # decorators = [auth.login_required]
    @auth.login_required
    def get(self):
        token = g.current_user.generate_auth_token(current_app)
        return jsonify({
            'token':token.decode('ascii')
        })

api.add_resource(UserApi, '/api/v0.1/user/')
api.add_resource(TokenApi, '/api/v0.1/user/token')
