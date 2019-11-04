# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from sqlalchemy import func, asc, desc
from server.module import db, api, multi_auth
from server.models.sales import SalesRecord, Agent, Contact
from flask import g, jsonify, current_app, request
import logging
import datetime
import time

logger = logging.getLogger(__name__)

class SalesList(Resource):
    decorators = [multi_auth.login_required]
    def post(slef):
        json = request.get_json(force=True)
        offset = int(json['offset']) if json['offset'] else 0
        limit = int(json['limit']) if json['limit'] else 20
        records = SalesRecord.query.order_by(desc(SalesRecord.id)).limit(limit).offset(offset)
        count = db.session.query(func.count(SalesRecord.id)).scalar()
        return jsonify({
            'record': [x.to_json() for x in records],
            'count': count,
            'status': 1
        })

class SalesAdd(Resource):
    decorators = [multi_auth.login_required]
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
                'message': "代理商: " + agent_name + " 不存在！"
            })
        contact_name = json['contact_name']
        contact = Contact.query.filter_by(name == contact_name).first()
        if not contact:
            return jsonify({
                'status': 0,
                'message': "代理商: " + contact_name + " 不存在！"
            })

        sales = SalesRecord()
        sales.nmuber = number
        sales.model = json['model']
        sales.quantity = json['quantity']
        sales.remarks = json['remarks']
        sales.agent_name = agent.name
        salse.contact_name = contact.name
        sales.contact_address = contact.address
        sales.contact_tel = contact.tel
        salse.operator = g.current_user.name
        salse.save()
        return jsonify({
            'status': 1,
            'message': '添加完成！'
        })

class AgentList(Resource):
    decorators = [multi_auth.login_required]
    def post(self):
        json = request.get_json(force=True)
        offset = int(json['offset']) if json['offset'] else 0
        limit = int(json['limit']) if json['limit'] else 20
        agents = Agent.query.order_by(desc(Agent.id)).limit(limit).offset(offset)
        count = db.session.query(func.count(Agent.id)).scalar()
        return jsonify({
            'agent': [x.to_json for x in agents],
            'count': count,
            'status': 1
        })

class AgentAdd(Resource):
    decorators = [multi_auth.login_required]
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
                'status': 1,
                'message': '新增代理商成功！'
            })
        return jsonify({
            'statue': 0,
            'message': "代理商: " + name + " 已存在！"
        })

class AgentListContact(Resource):
    decorators = [multi_auth.login_required]
    def get(self, agent_id):
        if agent_id:
            contacts = Contact.query.filter(Contact.agent_id == agent_id).order_by(desc(Contact.id)).all()
            return jsonify({
                'contact': [x.to_json() for x in contacts],
                'agent_id': agent_id,
                'status': 1
            })
        return jsonify({
            'status': 0,
            'message': '代理商不存在'
        })

class ContactAdd(Resource):
    decorators = [multi_auth.login_required]
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
