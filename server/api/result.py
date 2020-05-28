# -*- coding:utf-8 -*-

from flask import jsonify
from server.database import BaseModel

# successful
OK = 0

# error
ID_NOT_EXIST        = 10001
ID_ERROR            = 10002
PARAM_ERROR         = 10003
NAME_PASS_ERROR     = 10004
USER_NO_ACTIVE      = 10005
USER_EXIST          = 10006
USER_NO_EXIST       = 10007
DATA_NO_EXIST       = 10008
# other
UNKNOWN             = 20001

message = {
    OK              : '请求成功',
    ID_NOT_EXIST    : 'ID 不存在',
    ID_ERROR        : 'ID 错误',
    PARAM_ERROR     : '参数错误',
    NAME_PASS_ERROR : '用户名或密码错误',
    USER_NO_ACTIVE  : '用户未激活',
    USER_EXIST      : '用户已存在',
    USER_NO_EXIST   : '用户不存在',
    DATA_NO_EXIST   : '数据不存在',
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