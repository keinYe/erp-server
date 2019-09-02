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
from pycrawler.user.models import User
from flask_login import login_user
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

@impl
def hook_load_blueprints(app):
    user = Blueprint('user', __name__)
    register_view(user, routes=['/login'], view_func=Login.as_view('login'))
    app.register_blueprint(user, url_prefix='/user')
