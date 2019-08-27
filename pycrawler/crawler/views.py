# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.views import MethodView
from pycrawler.plugins import impl
from pycrawler.utils import register_view
from jinja2 import Markup

from pyecharts import options as opts
from pyecharts.charts import Bar

def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c


class Crawler(MethodView):
    def get(self):
        c = bar_base()
        return Markup(c.render_embed())

@impl
def hook_load_blueprints(app):
    crawler = Blueprint('crawler', __name__)
    register_view(crawler, routes=['/'], view_func=Crawler.as_view('index'))
    app.register_blueprint(crawler)
