# -*- coding:utf-8 -*-
import pytest
import json

def test_login(clinet):
    rv = clinet.post('/api/v01/user/login',
                    data=json.dumps(dict(user_name='test', password='test')),
                    content_type='application/json')
    data = json.loads(rv.data)

    assert rv.status_code == 200
    assert data['status'] == 1
    assert data['name'] == 'test'
    assert data['token'] is not None
    assert data['admin'] is not None
    assert data['expire'] is not None

def test_add_user(clinet, headers):

    rv = clinet.post('/api/v01/user',
                    data=json.dumps(dict(user_name='123', password='123', admin=False)),
                    headers=headers)
    data = json.loads(rv.data)
    assert rv.status_code == 200
    assert data['status'] == 1
