import os
import sys
import base64
import pprint

from gqylpy_datastruct import DataStruct

os.environ['MYSQL_USERNAME'] = 'gqylpy'
sys.argv.extend([
    '--mysql:password=5pS55Y+Y5LiW55WM44CC',
    '--mysql:autocommit'
])

branch       = 'branch'
items        = 'items'
coerce       = 'coerce'
default      = 'default'
env          = 'env'
option       = 'option'
enum         = 'enum'
verify       = 'verify'
optional     = 'optional'
option_bool  = 'option_bool'
callback     = 'callback'

re_ip     = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
re_domain = '^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'

blueprint = {
    'mysql': {
        branch: {
            'host': {type: str, verify: [re_ip, re_domain]},
            'port': {type: (int, str), coerce: int},
            'db': {type: str},
            'charset': {type: str, default: 'utf8mb4'},
            'username': {type: str, env: 'MYSQL_USERNAME'},
            'password': {
                type: str,
                option: '--mysql:password',
                callback: lambda x: base64.b64decode(x).decode()
            },
            'autocommit': {
                type: bool,
                coerce: bool,
                option_bool: '--mysql:autocommit'
            }
        }
    },
    'nodes': {
        items: {
            branch: {
                'ip': {type: str, verify: re_ip},
                'rules': {type: (str, list), set: ('master', 'node')},
                'type': {type: str, enum: ('host', 'vm')}
            }
        }
    }
}

data = {
    'mysql': {'host': 'gqylpy.com', 'port': 3306, 'db': 'gqylpy'},
    'nodes': [
        {'ip': '172.17.1.2', 'rules': ['master', 'node'], 'type': 'vm'},
        {'ip': '172.17.1.3', 'rules': 'node', 'type': 'host'},
        {'ip': '172.17.1.4', 'rules': 'node', 'type': 'host'}
    ]
}

datastruct = DataStruct(blueprint)
err = datastruct.verify(data)
pprint.pp(err or data)
