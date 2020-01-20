
import unittest
import os
from server import create_app
from server.module import db
from server.models.user import User, Permission
import tempfile
import json


DEFAULT_USERNAME = 'test'
DEFAULT_PASSWORD = 'test'

class ServerTestUser(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_file= tempfile.mkstemp()
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_file
        self.app = app
        self.clinet = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            user = User.create(
                name=DEFAULT_USERNAME,
                password=DEFAULT_PASSWORD,
                permission=Permission.ADMINISTRATOR,
                active=True)
            self.headers = self.login()


    def login(self):
        rv = self.clinet.post('/api/v01/user/login',
                               data=json.dumps(dict(user_name='test', password='test')),
                               content_type='application/json')
        data = json.loads(rv.data)
        token = data['token']
        headers = {"Authorization":"Bearer "+token, 'Content-Type': 'application/json'}
        return headers

    def test_login(self):
        rv = self.clinet.post('/api/v01/user/login',
                               data=json.dumps(dict(user_name=DEFAULT_PASSWORD, password=DEFAULT_PASSWORD)),
                               content_type='application/json')
        data = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(data['status'], 1)
        self.assertEqual(data['name'], 'test')
        self.assertIsNotNone(data['token'])
        self.assertIsNotNone(data['admin'])
        self.assertIsNotNone(data['expire'])

    def test_add_user(self):

        rv = self.clinet.post('/api/v01/user',
                               data=json.dumps(dict(user_name='123', password='123', admin=False)),
                               headers=self.headers)
        data = json.loads(rv.data)
        self.assertEqual(data['status'], 1)



    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_file)
