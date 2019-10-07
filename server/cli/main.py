# -*- coding:utf-8 -*-

import click, logging
from server import create_app
from flask.cli import FlaskGroup, ScriptInfo
from server.module import db
from sqlalchemy_utils import database_exists, create_database
from server.models.user import User, Permission

logger = logging.getLogger(__name__)

class ServerGroup(FlaskGroup):
    def __init__(self, *args, **kwargs):
        super(ServerGroup, self).__init__(*args, **kwargs)


def make_app(script_info):
    config_file = getattr(script_info, "config_file", None)
    return create_app(config_file)

def set_config(ctx, param, value):
    """This will pass the config file to the create_app function."""
    ctx.ensure_object(ScriptInfo).config_file = value


@click.group(cls=ServerGroup, create_app=make_app, add_version_option=False,
             invoke_without_command=True)
@click.option("--config", expose_value=False, callback=set_config,
              required=False, is_flag=False, is_eager=True, metavar="CONFIG",
              help="using a path like '/path/to/xxxx.cfg'")
@click.pass_context
def server(ctx):
    """This is the commandline interface for pycrawler."""
    if ctx.invoked_subcommand is None:
        # show the help text instead of an error
        # when just '--config' option has been provided
        click.echo(ctx.get_help())

@server.command('init', help="initialization databse")
# @click.option(help="initialization databse")
@click.option("--username", "-u", default='test', help="The username of the user.")
@click.option("--password", "-p", default='test', help="The password of the user.")
def install(username, password):
    if database_exists(db.engine.url):
        db.drop_all(bind=None)
    else:
        create_database(db.engine.url)
    db.create_all(bind=None)

    user = User.create(
        name=username,
        password=password,
        permission=Permission.ADMINISTRATOR,
        active=True)
