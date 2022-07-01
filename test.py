import os
import sys
import base64

from gqylpy_datastruct import DataStruct

data = {
    'mysql': {
        'host': 'gqylpy.com',
        'port': 3306,
        'db': 'gqylpy',
        'username': 'gqylpy',
        'password': '5pS55Y+Y5LiW55WM44CC',
    },
    'nodeInfo': [
        {'ip': '172.17.1.2', 'rules': ['master', 'node'], 'type': 'vm'},
        {'ip': '172.17.1.3', 'rules': 'node', 'type': 'host'},
        {'ip': '172.17.1.4', 'rules': 'node', 'type': 'host'}
    ]
}


data_blueprint = {
    'mysql': {
        'type': dict,
        'branch': {
            'host': {'type': str, 'verify': [r'\d+\.\d+\.\d+\.\d+', r'([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}']},
            'port': {'type': (int, str), 'coerce': int, 'verify': lambda x: 0 < x < 65536},
            'db': {'type': str},
            'charset': {'type': str, 'default': 'utf8'},
            'username': {'type': str},
            'password': {'type': str, 'callback': lambda x: base64.b64decode(x).decode()},
            'autocommit': {'type': bool, 'coerce': bool, 'default': False, 'option_bool': '--mysql:autocommit'},
        }
    },
    'nodeInfo': {
        'type': list,
        'items': {
            'type': dict,
            'branch': {
                'ip': {'type': str, 'verify': r'\d+\.\d+\.\d+\.\d+'},
                'rules': {'type': (str, list), 'set': ('master', 'node')},
                'type': {'type': str, 'enum': ('host', 'vm')}
            },
        }
    }
}

# branch, items, type, coerce, default, env:, option:, option_bool, enum, set, verify, callback

sys.argv.extend(['--mysql:autocommit'])

datastruct = DataStruct(data_blueprint)
datastruct.verify(data, eraise=True)
print(data)
