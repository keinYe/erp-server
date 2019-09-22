# -*- coding:utf-8 -*-

from flask import Flask, g, current_app
import logging
import logging.config
from .user.models import User
from pluggy import PluginManager
from pycrawler.plugins import spec
from pycrawler._compat import iteritems
import sys
from .module import (
    db,
    api,
    basic_auth,
    token_auth,
    migrate,
    login_manager,
)

from .template_filter import format_date
from flask_cors import CORS





logger = logging.getLogger(__name__)


def create_app(config=None):
    app = Flask(
        'pycrawler', instance_relative_config=True, static_folder="templates"
    )
    # cors = CORS(app, supports_credentials=True,resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app, supports_credentials=True)
    config_app(app, config)
    configure_pluggy(app)
    configure_module(app)
    configure_template_filters(app)

    return app

def config_app(app, config):
    app.config.from_object("pycrawler.configs.default.DefaultConfig")

    configure_logging(app)


def configure_module(app):
    # initialization database
    db.init_app(app)

    api.init_app(app)

    migrate.init_app(app, db)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        """Loads the user. Required by the `login` extension."""
        user_instance = User.query.filter_by(id=user_id).first()
        if user_instance:
            return user_instance
        else:
            return None

    login_manager.init_app(app, current_app)

def configure_pluggy(app):
    # iteritems = lambda d: d.iteritems()
    app.pluggy = PluginManager('pycrawler')
    app.pluggy.add_hookspecs(spec)

    modules = set(
        module
        for name, module in iteritems(sys.modules)
        if name.startswith("pycrawler")
    )
    for module in modules:
        app.pluggy.register(module)
    app.pluggy.hook.hook_load_blueprints(app=app)

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

def configure_template_filters(app):
    """Configures the template filters."""
    filters = {}

    filters["format_date"] = format_date

    app.jinja_env.filters.update(filters)


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
