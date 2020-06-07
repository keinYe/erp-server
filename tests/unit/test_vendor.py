# -*- coding:utf-8 -*-
import pytest
import json
from .common import (
    add_data_to_database,
    get_data_from_database,
    put_data_to_databse_id,
    get_data_from_database_id
)

def test_add_liaison(clinet, headers):
    data = {
        'name' : 'kein Ye',
        'tel' : '13000000000',
        'qq' : '463381729',
    }
    add_data_to_database(clinet, headers, '/api/v01/liaison', data)

def test_get_liaison(clinet, headers):
    get_data_from_database(clinet, headers, '/api/v01/liaison')

def test_get_liaison_from_id(clinet, headers):
    get_data_from_database_id(clinet, headers, '/api/v01/liaison')

def test_put_liaison_from_id(clinet, headers):
    put_data_to_databse_id(clinet, headers, '/api/v01/liaison')

def test_add_vendor(clinet, headers):
    data = {
        'name' : 'company',
        'address' : 'Guangdong, Shenzhen',
        'tax_number' : '3434343422222X',
        'liaison_id': 1,
    }
    add_data_to_database(clinet, headers, '/api/v01/vendor', data)

def test_get_vendor(clinet, headers):
    get_data_from_database(clinet, headers, '/api/v01/vendor')

def test_get_vendor_from_id(clinet, headers):
    get_data_from_database_id(clinet, headers, '/api/v01/vendor')

def test_put_vendor_from_id(clinet, headers):
    put_data_to_databse_id(clinet, headers, '/api/v01/vendor')


def test_get_vendor_check_data(clinet, headers):
    rv = clinet.get('/api/v01/vendor?offset=0&limit=20', headers=headers)

    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    data = result['data']
    assert data is not None
    vendors = data['vendors']
    for x in vendors:
        assert x.get('name', None) is not None
        assert x.get('address', None) is not None
        assert x.get('id', None) is not None
        assert x.get('tax_number', None) is not None
        assert x.get('liaison', None) is not None
        liaisons = x.get('liaison')
        for liaison in liaisons:
            assert liaison.get('id', None) is not None
            assert liaison.get('qq', None) is not None
            assert liaison.get('tel', None) is not None

