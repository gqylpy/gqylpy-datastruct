import os
import sys
import base64
import pprint

from gqylpy_datastruct import DataStruct

blueprint = {
    'mysql': {
        'type': dict,
        'branch': {
            'host': {'type': str, 'verify': [r'\d+\.\d+\.\d+\.\d+', r'([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}']},
            'port': {'type': (int, str), 'coerce': int, 'verify': lambda x: 0 < x < 65536},
            'db': {'type': str},
            'charset': {'type': str, 'default': 'utf8'},
            'username': {'type': str, 'env': 'MYSQL_USERNAME'},
            'password': {'type': str, 'option': '--mysql:password', 'callback': lambda x: base64.b64decode(x).decode()},
            'autocommit': {'type': bool, 'coerce': bool, 'option_bool': '--mysql:autocommit'}
        }
    },
    'nodes': {
        'type': 'list',
        'items': {
            'type': 'dict',
            'branch': {
                'ip': {'type': 'str', 'verify': r'\d+\.\d+\.\d+\.\d+'},
                'rules': {'type': ('str', 'list'), 'set': ('master', 'node')},
                'type': {'type': 'str', 'enum': ('host', 'vm')}
            }
        }
    }
}

data = {
    'mysql': {'host': 'gqylpy.com', 'port': '3306', 'db': 'gqylpy'},
    'nodes': [
        {'ip': '172.17.1.2', 'rules': ['master', 'node'], 'type': 'vm'},
        {'ip': '172.17.1.3', 'rules': 'node', 'type': 'host'},
        {'ip': '172.17.1.4', 'rules': 'node', 'type': 'host'}
    ]
}

os.environ['MYSQL_USERNAME'] = 'gqylpy'
sys.argv.extend([
    '--mysql:password=5pS55Y+Y5LiW55WM44CC',
    '--mysql:autocommit'
])

datastruct = DataStruct(blueprint)
err = datastruct.verify(data)
pprint.pp(err or data)
