# -*- coding:utf-8 -*-

from flask import Flask
import logging

from .module import (
    db,
    api,
)

logger = logging.getLogger(__name__)


def create_app(config=None):
    app = Flask(
        'pycrawler', instance_relative_config=True
    )
    config_app(app, config)
    configure_module(app)
    return app

def config_app(app, config):
    app.config.from_object("pycrawler.configs.default.DefaultConfig")


def configure_module(app):
    # initialization database
    db.init_app(app)

    api.init_app(app)
