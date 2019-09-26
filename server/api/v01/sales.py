from flask_restful import Resource, reqparse
from sqlalchemy import func
from server.module import db, api, multi_auth
from server.models.sales import SalesRecord, Agent, Contact
from flask import g, jsonify, current_app, request
import logging
import datetime
import time

logger = logging.getLogger(__name__)

class SalesList(Resource):
    @multi_auth.login_required
    def post(slef):
        json = request.get_json(force=True)
        offset = int(json['offset']) if json['offset'] else 0
        limit = int(json['limit']) if json['limit'] else 20
        records = SalesRecord.query.limit(limit).offset(offset)

        list = []
        for record in records:
            list.append({
                'id': record.id,
                'number': record.number,
                'date': record.date,
                'model': record.model,
                'quantity': record.quantity,
                'applicant': record.applicant,
                'agent_name': record.agent.name,
                'contact_name': record.contact.name,
                'contact_address': record.contact.address,
                'contact_tel': record.contact.address,
                'remarks': record.remarks
            })
        return jsonify({
            'record': list,
            'status': 1
        })


class SalesAdd(Resource):
    @multi_auth.login_required
    def post(self):
        json = request.get_json(force=True)
        number = json['number']
        sales = SalesRecord.query.filter_by(number == number).first()
        if sales:
            return jsonify({
                'status': 0,
                'message': "订单编号: " + number + " 已存在！"
            })
        agent_name = json['agent_name']
        agent = Agent.query.filter_by(name == agent_name).first()
        if not agent:
            return jsonify({
                'status': 0,
                'message': "代理商: " + agent_name + " 不已存在！"
            })
        contact_name = json['contact_name']
        contact = Contact.query.filter_by(name == contact_name).first()
        if not contact:
            return jsonify({
                'status': 0,
                'message': "代理商: " + contact_name + " 不已存在！"
            })

        sales = SalesRecord()
        sales.nmuber = number
        sales.model = json['model']
        sales.quantity = json['quantity']
        sales.remarks = json['remarks']
        sales.agent = agent
        salse.contact = contact
        salse.save()
        return jsonify({
            'status': 1
        })

class AgentList(Resource):
    @multi_auth.login_required
    def post(self):
        json = request.get_json(force=True)
        offset = int(json['offset']) if json['offset'] else 0
        limit = int(json['limit']) if json['limit'] else 20
        agents = Agent.query.limit(limit).offset(offset)
        list = []
        for agent in agents:
            contacts = []
            for contact in agent.contact:
                contacts.append({
                    'name': contact.name,
                    'address': contact.address,
                    'tel': contact.tel
                })
            list.append({
                'id': agent.id,
                'name': agent.name,
                'address': agent.address,
                'tel': agent.tel,
                'fax': agent.fax,
                'contact': contacts
            })
        return jsonify({
            'agent': list,
            'status': 1
        })

class AgentAdd(Resource):
    @multi_auth.login_required
    def post(self):
        json = request.get_json(force=True)
        name = json['name']
        agent = Agent.query.filter(Agent.name == name).first()
        if not agent:
            agent = Agent()
            agent.name = name
            agent.address = json['address']
            agent.tel = json['tel']
            agent.fax = json['fax']
            agent.save()
            return jsonify({
                'status': 1
            })
        return jsonify({
            'statue': 0,
            'message': "代理商: " + name + " 已存在！"
        })

class AgentListContact(Resource):
    @multi_auth.login_required
    def get(self, agent_id):
        if agent_id:
            contacts = Contact.query.filter(Contact.agent_id == agent_id).all()
            list = []
            for contact in contacts:
                list.append({
                    'id': contact.id,
                    'name': contact.name,
                    'address': contact.address,
                    'tel': contact.tel
            })
            return jsonify({
                'contact': list,
                'agent_id': agent_id,
                'status': 1
            })
        return jsonify({
            'status': 0
        })
class ContactAdd(Resource):
    @multi_auth.login_required
    def post(self):
        json = request.get_json(force=True)
        agent_name = json['agent_name']
        name = json['name']
        address = json['address']
        tel = json['tel']
        agent = Agent.query.filter(Agent.name == agent_name).first()
        if not agent:
            return jsonify({
                'status': 0,
                'message': "代理商: " + agent_name + " 不存在！"
            })
        contact = Contact.query.filter(Contact.name == name).first()
        if contact:
            return jsonify({
                'status': 0,
                'message': "联系人: " + name + " 已存在！"
            })
        contact = Contact()
        contact.name = name
        contact.address = address
        contact.tel = tel
        contact.agent = agent
        contact.save()
        return jsonify({
            'status': 1
        })

api.add_resource(SalesList, '/api/v01/order/list')
api.add_resource(SalesAdd, '/api/v01/order/add')
api.add_resource(AgentList, '/api/v01/order/agent/list')
api.add_resource(AgentAdd, '/api/v01/order/agent/add')
api.add_resource(AgentListContact, '/api/v01/order/agent/contact/<int:agent_id>')
api.add_resource(ContactAdd, '/api/v01/order/contact/add')
