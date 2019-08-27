# -*- coding:utf-8 -*-

import click
from pycrawler import create_app
from flask.cli import FlaskGroup, ScriptInfo

class PycrawlerGroup(FlaskGroup):
    def __init__(self, *args, **kwargs):
        super(PycrawlerGroup, self).__init__(*args, **kwargs)


def make_app(script_info):
    config_file = getattr(script_info, "config_file", None)
    return create_app(config_file)

def set_config(ctx, param, value):
    """This will pass the config file to the create_app function."""
    ctx.ensure_object(ScriptInfo).config_file = value


@click.group(cls=PycrawlerGroup, create_app=make_app, add_version_option=False,
             invoke_without_command=True)
@click.option("--config", expose_value=False, callback=set_config,
              required=False, is_flag=False, is_eager=True, metavar="CONFIG",
              help="using a path like '/path/to/xxxx.cfg'")
@click.pass_context
def pycrawler(ctx):
    """This is the commandline interface for pycrawler."""
    if ctx.invoked_subcommand is None:
        # show the help text instead of an error
        # when just '--config' option has been provided
        click.echo(ctx.get_help())
