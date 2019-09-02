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
from flask_login import login_required
import logging

logger = logging.getLogger(__name__)


class SalseList(MethodView):

    def get(self):
        return render_template('sales/list.html')

@impl
def hook_load_blueprints(app):
    sales = Blueprint('sales', __name__)
    register_view(sales, routes=['/list'], view_func=SalseList.as_view('list'))
    app.register_blueprint(sales, url_prefix='/sales')
