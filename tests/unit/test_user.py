# -*- coding:utf-8 -*-
import pytest
import json

def test_login(clinet):
    rv = clinet.post('/api/v01/user/login',
                    data=json.dumps(dict(user_name='test', password='test')),
                    content_type='application/json')
    result = json.loads(rv.data)

    assert rv.status_code == 200
    assert result['error_code'] == 0
    data = result['data']
    assert data['name'] == 'test'
    assert data['token'] is not None
    assert data['admin'] is not None
    assert data['expire'] is not None

def test_login_no_username(clinet):
    rv = clinet.post('/api/v01/user/login',
                    data=json.dumps(dict(user_name='test1', password='test')),
                    content_type='application/json')
    result = json.loads(rv.data)

    assert rv.status_code == 200
    assert result['error_code'] == 10004

    rv = clinet.post('/api/v01/user/login',
                    data=json.dumps(dict(user_name='test', password='test1')),
                    content_type='application/json')
    result = json.loads(rv.data)

    assert rv.status_code == 200
    assert result['error_code'] == 10004 

def test_no_login(clinet):
    username = '123'
    password = '123'

    rv = clinet.post('/api/v01/user',
                    data=json.dumps(dict(user_name=username, password=password, admin=False)))
    assert rv.status_code == 401

def test_add_user(clinet, headers):
    username = '123'
    password = '123'

    rv = clinet.post('/api/v01/user',
                    data=json.dumps(dict(user_name=username, password=password, admin=False)),
                    headers=headers)
    result = json.loads(rv.data)
    assert rv.status_code == 200
    assert result['error_code'] == 0

    rv = clinet.post('/api/v01/user/login',
                    data=json.dumps(dict(user_name=username, password=password)),
                    content_type='application/json')
    result = json.loads(rv.data)

    assert rv.status_code == 200
    assert result['error_code'] == 10005

def test_add_user_exist(clinet, headers):
    username = '123'
    password = '123'
    rv = clinet.post('/api/v01/user',
                    data=json.dumps(dict(user_name=username, password=password, admin=False)),
                    headers=headers)
    result = json.loads(rv.data)
    assert rv.status_code == 200
    assert result['error_code'] == 10006

def test_get_user_list(clinet, headers):
    rv = clinet.get('/api/v01/user?offset=0&limit=20',
                    headers=headers)
    
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    data = result['data']
    assert data['count'] is not None
    assert isinstance(data['users'], list)

def test_get_user_form_id(clinet, headers):
    rv = clinet.get('/api/v01/user/2',
                    headers=headers)    
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0

def test_get_user_from_id_no_exist(clinet, headers):
    rv = clinet.get('/api/v01/user/100',
                    headers=headers)    
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10007


def test_user_dyn(clinet, headers):
    rv = clinet.post('/api/v01/user/dyn',
                    data=json.dumps(dict(data=100)),
                    content_type='application/json')
    assert rv.status_code == 401

    rv = clinet.post('/api/v01/user/dyn',
                    data=json.dumps(dict(data=None)),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10008

    
    rv = clinet.post('/api/v01/user/dyn',
                    data=json.dumps(dict(data=100)),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    
    rv = clinet.get('/api/v01/usr/dyn',
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['data'] == 100