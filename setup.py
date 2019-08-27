# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name='pycrawler',
    version='0.0.1',
    entry_points="""
        [console_scripts]
        pycrawler=pycrawler.cli:pycrawler
    """,

)
