from flask import Blueprint,request
from flask.views import MethodView
from pycrawler.plugins import impl
from pycrawler.utils import register_view
from pyecharts import options as opts
from pyecharts.charts import Bar
from pycrawler.crawler.models import Brands, Catalog, Materials
from pycrawler.module import db
from flask import render_template, jsonify
import logging

logger = logging.getLogger(__name__)


class BrandBar(MethodView):
    def get(self):
        brands = [name[0] for name in db.session.query(Brands.name).all()]
        # brands = db.session.query(Brands).all()
        return render_template('brand_bar.html', brands=brands)

    def post(self):
        jsons = request.get_json(force=True)
        brand_name = jsons['name']
        brand_id = db.session.query(Brands.id).filter(Brands.name == brand_name).one()[0]

        catalog_ids = db.session.query(Catalog.id, Catalog.name).filter(Catalog.parent_id==None).all()

        catalog_name = []
        catalog_count = []
        for cata_id, name in catalog_ids:
            catalog_name.append(name)
            count = db.session.query(Materials).join(Catalog).filter(
                    Materials.brand_id == brand_id).filter(
                    Catalog.parent_id == cata_id).count()
            catalog_count.append(count)

        c = (
            Bar()
            .add_xaxis(catalog_name)
            .add_yaxis('数量', catalog_count)
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)),
                title_opts=opts.TitleOpts(title=brand_name, subtitle="物料数量"),
            )
        )
        return c.dump_options_with_quotes()


@impl
def hook_load_blueprints(app):
    brand = Blueprint('brand', __name__)
    register_view(brand, routes=['/bar'], view_func=BrandBar.as_view('index'))
    app.register_blueprint(brand, url_prefix='/brand')
