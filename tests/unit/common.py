# -*- coding:utf-8 -*-
import pytest
import json

def add_data_to_database(clinet, headers, url, data={'name':'data'}):
    rv = clinet.post(url)
    assert rv.status_code == 401

    rv = clinet.post(url,
                    data=json.dumps(dict(data=None)),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10008

    rv = clinet.post(url,
                    data=json.dumps(data),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    assert isinstance(result['data'], dict)

    rv = clinet.post(url,
                    data=json.dumps(data),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10009   

def get_data_from_database(clinet, headers, url):
    rv = clinet.get(url)
    assert rv.status_code == 401

    rv = clinet.get(url,
                    headers=headers)
    assert rv.status_code == 400

    rv = clinet.get(url + '?offset=0&limit=20',
                    headers=headers)
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    data = result['data']
    assert isinstance(data['count'], int)

def get_data_from_database_id(clinet, headers, url, id=1):
    rv = clinet.get(url + '/' + str(id))
    assert rv.status_code == 401

    rv = clinet.get(url + '/' +  str(id),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    assert result['data'] is not None

    rv = clinet.get(url + '/' +  str(4030),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10001

def put_data_to_databse_id(clinet, headers, url, id=1, data=None):
    if data is None:
        data = {'name' : '123'}
    rv = clinet.put(url + '/' +  str(id),
                    data=json.dumps(dict(name=None)))
    assert rv.status_code == 401

    rv = clinet.put(url + '/' +  str(id),
                    data=json.dumps(data),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    assert result['data'] is not None

    rv = clinet.put(url + '/' +  str(4030),
                    data=json.dumps(data),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10001