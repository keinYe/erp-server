# -*- coding:utf-8 -*-

import os
import tempfile
import pytest
import json
from server import create_app
from server.module import db
from server.models.user import User, Permission

DEFAULT_USERNAME = 'test'
DEFAULT_PASSWORD = 'test'

@pytest.fixture(scope='session')
def app():
    db_fd, db_file = tempfile.mkstemp()
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file

    print('pytest start')

    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User.create(
            name=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD,
            permission=Permission.ADMINISTRATOR,
            active=True)

    yield app
    print('pytest stop')
    with app.app_context():
        db.session.remove()
        db.drop_all()
    os.close(db_fd)
    os.unlink(db_file)

@pytest.fixture
def clinet(app):
    return app.test_client()

@pytest.fixture
def headers(app, clinet):
    rv = clinet.post('/api/v01/user/login',
                        data=json.dumps(dict(user_name='test', password='test')),
                        content_type='application/json')
    data = json.loads(rv.data)
    token = data['token']
    headers = {"Authorization":"Bearer "+token, 'Content-Type': 'application/json'}

    yield headers

    pass
