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
from .models import Agent, Contact
from sqlalchemy import asc, desc

logger = logging.getLogger(__name__)


class AgentList(MethodView):

    def get(self):
        page = request.args.get("page", 1, type=int)
        agents = Agent.query.order_by(desc(SalesRecord.id)).paginate(
            page, 30, False
        )
        return render_template('agent/agent_list.html', agents=agents)

@impl
def hook_load_blueprints(app):
    agent = Blueprint('agent', __name__)
    register_view(agent, routes=['/list'], view_func=Agent.as_view('list'))
    app.register_blueprint(sales, url_prefix='/agent')
