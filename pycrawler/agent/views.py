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
        agents = Agent.query.order_by(desc(Agent.id)).paginate(
            page, 30, False
        )
        return render_template('agent/list.html', agents=agents)

class AgentAdd(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('agent/add_agent.html')

    def post(self):
        json = request.get_json(force=True)
        name = json['name']
        address = json['address']
        tel = json['tel']
        if name and address and tel:
            agent = Agent()
            agent.name = name
            agent.address = address
            agent.tel = tel
            agent.fax = json['fax']
            agent.save()
            return jsonify({'status':302, 'location':'/agent/list'})
        return render_template('agent/add_agent.html')

class ContactAdd(MethodView):
    decorators = [login_required]

    def get(self):
        agents = Agent.query.all()
        return render_template('agent/add_contact.html', agents=agents)

    def post(self):
        json = request.get_json(force=True)
        name = json['name']
        address = json['address']
        tel = json['tel']
        if name and address and tel:
            contact = Contact()
            contact.name = name
            contact.address = address
            contact.tel = tel
            agent_name = json['agent']
            if agent_name:
                agent = Agent.query.filter(Agent.name.like('%'+agent_name+'%')).first()
                if agent:
                    contact.agent = agent
            contact.save()
            return jsonify({'status':302, 'location':'/agent/list'})
        return render_template('agent/add_contact.html')

class ContactList(MethodView):

    def get(self):
        page = request.args.get("page", 1, type=int)
        contacts = Contact.query.order_by(desc(Contact.id)).paginate(
            page, 30, False
        )
        return render_template('agent/list_contact.html', contacts=contacts)


@impl
def hook_load_blueprints(app):
    agent = Blueprint('agent', __name__)
    register_view(agent, routes=['/list'], view_func=AgentList.as_view('list'))
    register_view(agent, routes=['/add/agent'], view_func=AgentAdd.as_view('add_agent'))
    register_view(agent, routes=['/add/contact'], view_func=ContactAdd.as_view('add_contact'))
    register_view(agent, routes=['/list/contact'], view_func=ContactList.as_view('list_contact'))
    app.register_blueprint(agent, url_prefix='/agent')
