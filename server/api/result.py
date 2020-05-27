# -*- coding:utf-8 -*-

from flask import jsonify
from server.database import BaseModel

# successful
OK = 0

# error
ID_NOT_EXIST        = 10001
ID_ERROR            = 10002
PARAM_ERROR         = 10003
# other
UNKNOWN             = 20001

message = {
    OK              : '请求成功',
    ID_NOT_EXIST    : 'ID 不存在',
    ID_ERROR        : 'ID 错误',
    PARAM_ERROR     : '参数错误',
    UNKNOWN         : '未知错误'
}

def create_response(code, count=0, data=None, show=None, _hide=[], _path=None):
    if data:
        if isinstance(data, BaseModel) and hasattr(data, 'to_dict'):
            to_dict = getattr(data, 'to_dict')
            return jsonify({
                'error_code': code,
                'message': message.get(code, '未知错误'),
                'data': to_dict(show, _hide, _path)
            })
        elif isinstance(data, dict) or isinstance(data, list):
            return jsonify({
                'error_code': code,
                'message': message.get(code, '未知错误'),
                'data': data
            })
        else:
            return jsonify({
                'error_code': UNKNOWN,
                'message': message.get(UNKNOWN, '未知错误'),
                'data': {}
            })

    return jsonify({
        'error_code':code,
        'message': message.get(code, '未知错误'),
        'data': {}
    })    