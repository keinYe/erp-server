# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name='server',
    version='0.0.1',
    entry_points="""
        [console_scripts]
        server=server.cli:server
    """,

)
