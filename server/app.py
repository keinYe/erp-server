# -*- coding:utf-8 -*-

from flask import Flask, g, current_app
import logging
import logging.config
from server.models.user import User
from ._compat import iteritems
import sys
from .module import (
    db,
    api,
    basic_auth,
    token_auth,
    migrate,
)

from flask_cors import CORS

logger = logging.getLogger(__name__)

def create_app(config=None):
    app = Flask(
        'pycrawler', instance_relative_config=True, static_folder="templates"
    )
    # cors = CORS(app, supports_credentials=True,resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app, supports_credentials=True)
    config_app(app, config)
    configure_module(app)

    return app

def config_app(app, config):
    app.config.from_object("server.configs.default.DefaultConfig")

    configure_logging(app)


def configure_module(app):
    # initialization database
    db.init_app(app)

    api.init_app(app)

    migrate.init_app(app, db)

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
    if app.config["SEND_LOGS"]:
        configure_mail_logs(app)

@basic_auth.verify_password
def verify_password(username, password):
    g.current_user = None
    user = User.query.filter_by(name = username).first()
    if not user or not user.check_password(password):
        return False
    g.current_user = user
    return True


@token_auth.verify_token
def verify_token(token):
    g.current_user = None
    user = User.verify_auth_token(token, current_app)
    if not user:
        return False
    g.current_user = user
    return True

# @multi_auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
#     user = User.verify_auth_token(username_or_token, current_app)
#     logger.info('username:{} password:{}'.format(username_or_token, password))
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(name = username_or_token).first()
#         if not user or not user.check_password(password):
#             return False
#     g.current_user = user
#     return True
