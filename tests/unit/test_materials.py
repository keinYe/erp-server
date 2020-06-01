# -*- coding: utf-8 -*-
import pytest
import json


def test_add_category(clinet, headers):
    rv = clinet.post('/api/v01/categorys')
    assert rv.status_code == 401

    rv = clinet.post('/api/v01/categorys',
                    data=json.dumps(dict(data=None)),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10008

    rv = clinet.post('/api/v01/categorys',
                    data=json.dumps(dict(name='PCB')),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    assert isinstance(result['data'], dict)

def test_get_category(clinet, headers):
    rv = clinet.get('/api/v01/categorys')
    assert rv.status_code == 401

    rv = clinet.get('/api/v01/categorys',
                    headers=headers)
    assert rv.status_code == 400

    rv = clinet.get('/api/v01/categorys?offset=0&limit=20',
                    headers=headers)
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    data = result['data']
    assert isinstance(data['count'], int)
    assert data['category'] is not None

def test_get_category_id(clinet, headers):
    rv = clinet.get('/api/v01/categorys/1')
    assert rv.status_code == 401

    rv = clinet.get('/api/v01/categorys/1',
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    assert result['data'] is not None

    rv = clinet.get('/api/v01/categorys/100',
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10001    

def test_post_category_id(clinet, headers):
    rv = clinet.post('/api/v01/categorys/1',
                    data=json.dumps(dict(name=None)))
    assert rv.status_code == 401

    rv = clinet.post('/api/v01/categorys/1',
                    data=json.dumps(dict(name=None)),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10008

    rv = clinet.post('/api/v01/categorys/1',
                    data=json.dumps(dict(name='PCB')),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    assert result['data'] is not None

    rv = clinet.post('/api/v01/categorys/100',
                    data=json.dumps(dict(name='PCB')),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10001        