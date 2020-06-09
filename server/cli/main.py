# -*- coding:utf-8 -*-
import binascii
import click, logging, os, sys
from datetime import datetime
from server import create_app
from flask.cli import FlaskGroup, ScriptInfo
from server.module import db
from sqlalchemy_utils import database_exists, create_database
from server.models.user import User, Permission
from jinja2 import Environment, FileSystemLoader
from flask import current_app

logger = logging.getLogger(__name__)




class ServerGroup(FlaskGroup):
    def __init__(self, *args, **kwargs):
        super(ServerGroup, self).__init__(*args, **kwargs)

def prompt_config_path(config_path):
    """Asks for a config path. If the path exists it will ask the user
    for a new path until a he enters a path that doesn't exist.
    :param config_path: The path to the configuration.
    """
    click.secho("The path to save this configuration file.", fg="cyan")
    while True:
        if os.path.exists(config_path) and click.confirm(click.style(
            "Config {cfg} exists. Do you want to overwrite it?"
            .format(cfg=config_path), fg="magenta")
        ):
            break

        config_path = click.prompt(
            click.style("Save to", fg="magenta"),
            default=config_path)

        if not os.path.exists(config_path):
            break

    return config_path


def write_config(config, config_template, config_path):
    """Writes a new config file based upon the config template.
    :param config: A dict containing all the key/value pairs which should be
                   used for the new configuration file.
    :param config_template: The config (jinja2-)template.
    :param config_path: The place to write the new config file.
    """
    with open(config_path, 'wb') as cfg_file:
        cfg_file.write(
            config_template.render(**config).encode("utf-8")
        )

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
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
        db.create_all()
    if database_exists(db.engine.url):
        user = User.query.filter_by(name=username).first()
        if user:
            user.password = password
        else:
            user = User.create(
                name=username,
                password=password,
                permission=Permission.ADMINISTRATOR,
                active=True)
        user.save()
    else:
        click.secho("User table does not exists, please create User table!")

@server.command("makeconfig")
@click.option("--development", "-d", default=False, is_flag=True,
              help="Creates a development config with DEBUG set to True.")
@click.option("--output", "-o", required=False,
              help="The path where the config file will be saved at. "
                   "Defaults to the server's root folder.")
@click.option("--force", "-f", default=False, is_flag=True,
              help="Overwrite any existing config file if one exists.")
def generate_config(development, output, force):
    """Generates a Server configuration file."""
    config_env = Environment(
        loader=FileSystemLoader(os.path.join(current_app.root_path, "configs"))
    )
    config_template = config_env.get_template('config.cfg.template')

    if output:
        config_path = os.path.abspath(output)
    else:
        config_path = os.path.dirname(current_app.root_path)

    if os.path.exists(config_path) and not os.path.isfile(config_path):
        config_path = os.path.join(config_path, "erp-server.cfg")

    # An override to handle database location paths on Windows environments
    database_path = "sqlite:///" + os.path.join(
        os.path.dirname(current_app.instance_path), "erp-server.sqlite")
    if os.name == 'nt':
        database_path = database_path.replace("\\", r"\\")

    default_conf = {
        "is_debug": False,
        "database_uri": database_path,
        "secret_key": binascii.hexlify(os.urandom(24)).decode(),
        "csrf_secret_key": binascii.hexlify(os.urandom(24)).decode(),
        "timestamp": datetime.utcnow().strftime("%A, %d. %B %Y at %H:%M"),
        "log_config_path": "",
        "deprecation_level": "default"
    }

    if not force:
        config_path = prompt_config_path(config_path)

    if force and os.path.exists(config_path):
        click.secho("Overwriting existing config file: {}".format(config_path),
                    fg="yellow")
    if development:
        default_conf["is_debug"] = True
        write_config(default_conf, config_template, config_path)
        sys.exit(0)
    # SQLALCHEMY_DATABASE_URI
    click.secho("For more options see the SQLAlchemy docs:\n"
                "    http://docs.sqlalchemy.org/en/latest/core/engines.html",
                fg="cyan")
    default_conf["database_uri"] = click.prompt(
        click.style("Database URI", fg="magenta"),
        default=default_conf.get("database_uri"))

    write_config(default_conf, config_template, config_path)
    # Finished
    click.secho("The configuration file has been saved to:\n{cfg}\n"
                "Feel free to adjust it as needed."
                .format(cfg=config_path), fg="blue", bold=True)
    click.secho("Usage: \nserver --config {cfg} run"
                .format(cfg=config_path), fg="green")
