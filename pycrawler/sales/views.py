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
from .models import SalesRecord
from sqlalchemy import asc, desc
import datetime

logger = logging.getLogger(__name__)

class SalesEdit(MethodView):

    def get(self):
        record_id = request.args.get("id", 1, type=int)
        if record_id:
            record = SalesRecord.query.filter(SalesRecord.id == record_id).first()
            return render_template('sales/edit.html', record=record)
        return render_template('sales/add.html')

    def post(self):
        return redirect(url_for('sales.list'))

class SalseList(MethodView):

    def get(self):
        logger.info('test')
        page = request.args.get("page", 1, type=int)
        records = SalesRecord.query.order_by(desc(SalesRecord.id)).paginate(
            page, 30, False
        )
        logger.info(records)
        # for record in records:
        #     logger.info(record)
        return render_template('sales/list.html', records=records)

class SalesAdd(MethodView):

    def get(self):
        return render_template('sales/add.html')

    def post(self):
        json = request.get_json(force=True)
        logger.info(json)
        model = json['model']
        quantity = int(json['quantity'])
        applicant = json['applicant']
        contact = json['contact']
        if model and quantity and applicant and contact:
            sales = SalesRecord()
            sales.date = datetime.datetime.utcnow()
            sales.device_model = model
            sales.quantity = quantity
            sales.agent = json['agent']
            sales.contact = contact
            sales.applicant = applicant
            sales.address = json['address']
            sales.tel = json['tel']
            sales.remarks = json['remarks']
            sales.save()
            return redirect(url_for('sales.list'))
        return render_template('sales/add.html')

@impl
def hook_load_blueprints(app):
    sales = Blueprint('sales', __name__)
    register_view(sales, routes=['/list'], view_func=SalseList.as_view('list'))

    register_view(sales, routes=['/add'], view_func=SalesAdd.as_view('add'))

    register_view(sales, routes=['/edit'], view_func=SalesEdit.as_view('edit'))
    app.register_blueprint(sales, url_prefix='/sales')
