# -*- coding:utf-8 -*-

def register_view(bp_or_app, routes, view_func, *args, **kwargs):
    for route in routes:
        bp_or_app.add_url_rule(route, view_func=view_func, *args, **kwargs)
