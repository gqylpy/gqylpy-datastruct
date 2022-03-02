import base64
from isddc_datastruct import DataBlueprint

blueprint = {
    'mysql': {
        'type': dict,
        'branch': {
            'host': {'type': str, 'default': 'isddc-mysql', 'env': 'MYSQL_HOST'},
            'port': {'type': (int, str), 'default': 3306, 'coerce': int, 'env': 'MYSQL_PORT'},
            'db': {'type': str, 'default': 'isddc', 'env': 'MYSQL_DB'},
            'username': {'type': str, 'default': 'isddc', 'env': 'MYSQL_USERNAME'},
            'password': {'type': str, 'env': 'MYSQL_PASSWORD', 'callback': lambda x: base64.b64decode(x).decode()},
            'charset': {'type': str, 'default': 'utf8'},
        }
    },
    'nodeList': {
        'type': 'list',
        'items': {
            'type': 'dict',
            'branch': {
                'address': {'type': 'str', 'verify': ['\d+\.\d+\.\d+\.\d+', '([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}']},
                'username': {'type': 'str', 'default': 'root'},
                'password': {'type': 'str', 'callback': lambda x: base64.b64decode(x).decode()},
                'rules': {'type': ('list', 'str'), 'set': ('master', 'node')},
                'type': {'type': 'str', 'default': 'host', 'enum': ('host', 'vm')}
            }
        }
    },
    'timeout': {
        'type': ('int', 'str'),
        'default': 15,
        'coerce': 'int',
        'option': '--timeout',
    }
}
data = {
    'mysql': {
        'host': 'isddc-mysql',
        'port': '3306',
        'db': 'mon',
        'username': 'isddc',
        'password': 'cGFzc0B3MHJk',
    },
    'nodeList': [
        {
            'address': 'dev.isddc.com',
            'username': 'root',
            'password': 'cGFzc0B3MHJk',
            'rules': ['master', 'node'],
            'type': 'vm'
        },
        {
            'address': '192.168.1.11',
            'username': 'root',
            'password': 'cGFzc0B3MHJk',
            'rules': 'node'
        },
        {
            'address': '192.168.1.12',
            'username': 'root',
            'password': 'cGFzc0B3MHJk',
            'rules': 'node'
        }
    ]
}

datastruct = DataBlueprint(blueprint)
err: dict = datastruct.verify(data)

print(err or data)
