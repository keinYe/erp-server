# -*- coding:utf-8 -*-

from flask import Blueprint
from flask.views import MethodView
from pycrawler.plugins import impl
from pycrawler.utils import register_view
from flask import (
    render_template,
    jsonify,
    redirect,
    url_for,
    request,
)
from sqlalchemy import asc, desc
from pycrawler.user.models import User
from flask_login import login_user, logout_user, login_required
import logging

logger = logging.getLogger(__name__)

class Login(MethodView):
    def get(self):
        return render_template('user/login.html')

    def post(self):
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        logger.info(remember)
        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next = request.args.get('next')
            return redirect(next or url_for('brand.bar'))
        return render_template('user/login.html')

class Logout(MethodView):
    decorators = [login_required]

    def get(self):
        logout_user()
        return redirect(url_for('user.login'))

class List(MethodView):
    decorators = [login_required]

    def get(self):
        page = request.args.get("page", 1, type=int)
        users = User.query.order_by(desc(User.id)).paginate(
            page, 30, False
        )
        return render_template('user/list.html', users=users)

class Add(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('user/add.html')

    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username == username).first()
        if user is not None:
            user = User()
            user.username = username
            user.password = password
            user.save()
            return redirect(url_for('user.list'))
        return render_template('user/login.html')

@impl
def hook_load_blueprints(app):
    user = Blueprint('user', __name__)
    register_view(user, routes=['/login'], view_func=Login.as_view('login'))
    register_view(user, routes=['/logout'], view_func=Logout.as_view('logout'))
    register_view(user, routes=['/list'], view_func=List.as_view('list'))
    register_view(user, routes=['/add'], view_func=Add.as_view('add'))
    app.register_blueprint(user, url_prefix='/user')
