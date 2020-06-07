# -*- coding: utf-8 -*-
import pytest
import json
from .common import (
    add_data_to_database,
    get_data_from_database,
    put_data_to_databse_id,
    get_data_from_database_id
)

def test_add_category(clinet, headers):
    data = {
        'name': 'PCB',
        'encode_rules': '20001000000'
    }
    add_data_to_database(clinet, headers, '/api/v01/categorys', data)

def test_get_category(clinet, headers):
    get_data_from_database(clinet, headers, '/api/v01/categorys')

def test_get_category_id(clinet, headers):
    get_data_from_database_id(clinet, headers, '/api/v01/categorys')

def test_put_category_id(clinet, headers):
    put_data_to_databse_id(clinet, headers, '/api/v01/categorys')

def test_add_manufacturer(clinet, headers):
    add_data_to_database(clinet, headers, '/api/v01/manufacturer') 

def test_get_manufacturer(clinet, headers):
    get_data_from_database(clinet, headers, '/api/v01/manufacturer')

def test_get_manufacturer_id(clinet, headers):
    get_data_from_database_id(clinet, headers, '/api/v01/manufacturer')
    
def test_put_manufacturer_id(clinet, headers):
    put_data_to_databse_id(clinet, headers, '/api/v01/manufacturer')

def test_add_material(clinet, headers):
    data = {
        'serial' : '1000011',
        'manu_serial' : '111111111',
        'desc' : 'is a ?',
        'category_id' : 1,
        'manufacturer_id' : 1
    }

    rv = clinet.post('/api/v01/materials')
    assert rv.status_code == 401

    rv = clinet.post('/api/v01/materials',
                    data=json.dumps(dict(data=None)),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10008

    rv = clinet.post('/api/v01/materials',
                    data=json.dumps(data),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    assert isinstance(result['data'], dict)

    rv = clinet.post('/api/v01/materials',
                    data=json.dumps(data),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10009  


def test_get_material(clinet, headers):
    get_data_from_database(clinet, headers, '/api/v01/materials')

def test_get_material_id(clinet, headers):
    get_data_from_database_id(clinet, headers, '/api/v01/materials')

def test_put_material_id(clinet, headers):
    data = {
        'serial' : '1000011',
        'manu_serial' : '111111111',
        'desc' : 'is a ?',
        'category_id' : 1,
        'manufacturer_id' : 1
    }
    rv = clinet.put('/api/v01/materials' + '/' +  str(1),
                    data=json.dumps(dict(name=None)))
    assert rv.status_code == 401

    rv = clinet.put('/api/v01/materials' + '/' +  str(1),
                    data=json.dumps(data),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 0
    assert result['data'] is not None

    rv = clinet.put('/api/v01/materials' + '/' +  str(4030),
                    data=json.dumps(data),
                    headers=headers)
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert result['error_code'] == 10001
