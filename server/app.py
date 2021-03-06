# -*- coding:utf-8 -*-

from flask import Flask, g, current_app
import logging
import logging.config
from server.models.user import User
from ._compat import iteritems
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sys, time
from .module import (
    db,
    api,
    basic_auth,
    token_auth,
    migrate,
    redis_client,
)


from flask_cors import CORS

logger = logging.getLogger(__name__)

def create_app(config=None):
    app = Flask(
        'server', instance_relative_config=True
    )
    # cors = CORS(app, supports_credentials=True,resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app, supports_credentials=True)
    config_app(app, config)
    configure_module(app)

    return app

def config_app(app, config):
    if config is None:
        app.config.from_object("server.configs.default.DefaultConfig")
    else:
        app.config.update(config)

    configure_logging(app)


def configure_module(app):
    # initialization database
    db.init_app(app)

    api.init_app(app)

    migrate.init_app(app, db)

    redis_client.init_app(app)

def configure_logging(app):
    """Configures logging."""
    if app.config.get("USE_DEFAULT_LOGGING"):
        configure_default_logging(app)

    if app.config.get("LOG_CONF_FILE"):
        logging.config.fileConfig(
            app.config["LOG_CONF_FILE"], disable_existing_loggers=False
        )

    if app.config["SQLALCHEMY_ECHO"]:
        # Ref: http://stackoverflow.com/a/8428546
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(
            conn, cursor, statement, parameters, context, executemany
        ):
            conn.info.setdefault("query_start_time", []).append(time.time())

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(
            conn, cursor, statement, parameters, context, executemany
        ):
            total = time.time() - conn.info["query_start_time"].pop(-1)
            app.logger.debug("Total Time: %f", total)


def configure_default_logging(app):
    # Load default logging config
    logging.config.dictConfig(app.config["LOG_DEFAULT_CONF"])

@basic_auth.verify_password
def verify_password(username, password):
    g.current_user = None
    user = User.query.filter_by(name = username).first()
    if not user or not user.check_password(password) or not user.isActive():
        return False
    g.current_user = user
    return True


@token_auth.verify_token
def verify_token(token):
    g.current_user = None
    user = User.verify_auth_token(token, current_app)
    if not user or not user.isActive():
        return False
    g.current_user = user
    return True
