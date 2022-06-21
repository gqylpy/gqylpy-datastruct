"""
─────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████───████████──████████─██████─────────██████████████─████████──████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░██──██░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░██──██░░░░██─
─██░░██████████─██░░██████░░██───████░░██──██░░████─██░░██─────────██░░██████░░██─████░░██──██░░████─
─██░░██─────────██░░██──██░░██─────██░░░░██░░░░██───██░░██─────────██░░██──██░░██───██░░░░██░░░░██───
─██░░██─────────██░░██──██░░██─────████░░░░░░████───██░░██─────────██░░██████░░██───████░░░░░░████───
─██░░██──██████─██░░██──██░░██───────████░░████─────██░░██─────────██░░░░░░░░░░██─────████░░████─────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██████████───────██░░██───────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██───────────────██░░██───────
─██░░██████░░██─██░░██████░░████───────██░░██───────██░░██████████─██░░██───────────────██░░██───────
─██░░░░░░░░░░██─██░░░░░░░░░░░░██───────██░░██───────██░░░░░░░░░░██─██░░██───────────────██░░██───────
─██████████████─████████████████───────██████───────██████████████─██████───────────────██████───────
─────────────────────────────────────────────────────────────────────────────────────────────────────

Copyright © 2022 GQYLPY. 竹永康 <gqylpy@outlook.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import re
import copy
import datetime as dt

import gqylpy_exception as ge
import gqylpy_option    as gopt
import gqylpy_import    as gimport

module = os.__class__

unique = 'gqylpy-d82644a2db26dbd60b039c79d'

coerces_supported = int, str, list, tuple, set, dict, bool
types_supported = coerces_supported + (dt.date, dt.time, dt.datetime)

coerces = {}
for i in coerces_supported:
    coerces[i] = i
    coerces[i.__name__] = i

types = {}
for i in types_supported:
    types[i] = i
    types[i.__name__] = i

coerces_supported = [i.__name__ for i in coerces_supported]
types_supported = [i.__name__ for i in types_supported]


class DataBlueprint:

    def __init__(self, blueprint: dict):
        if blueprint.__class__ is not dict:
            x: str = blueprint.__class__.__name__
            raise ge.BlueprintTypeError(f'Blueprint type must be a "dict", not "{x}".')

        self.blueprint = copy.deepcopy(blueprint)

        for key, sub_blueprint in self.blueprint.items():
            self.decompose(key, sub_blueprint)

    def __iter__(self):
        yield from self.blueprint.items()

    def verify(self, data: dict, *, else_raise: bool = False) -> (dict, None):
        return DataValidator(data, self).verify(else_raise=else_raise)

    def decompose(self, keypath: str, blueprint: dict, *, elif_: bool = False):
        if blueprint.__class__ is not dict:
            x: str = blueprint.__class__.__name__
            raise ge.BlueprintStructureError({
                'keypath': keypath,
                'msg': f'Blueprint structure must be defined using "dict", not "{x}".'
            })

        branch, items = blueprint.get('branch'), blueprint.get('items')

        if not elif_:
            for key, value in blueprint.items():
                if key not in ('branch', 'items', 'default') and value:
                    try:
                        verify_func = getattr(self, f'verify_{key}')
                    except AttributeError:
                        raise ge.BlueprintVerifyMethodError({
                            'keypath': keypath,
                            'verify_method': key,
                            'msg': f'There is no "{key}" verification method.'
                        })
                    verify_func(keypath, key, value, blueprint)

        if branch and items:
            raise ge.BlueprintLimbError({
                'keypath': keypath,
                'msg': '"branch" and "items" cannot exist together.'
            })
        if branch:
            self.check_limb(keypath, branch, 'branch', blueprint)
            for key, sub_blueprint in branch.items():
                self.decompose(f'{keypath}.branch.{key}', sub_blueprint)
        elif items:
            self.check_limb(keypath, items, 'items', blueprint)
            self.decompose(f'{keypath}.items', items, elif_=True)

    @staticmethod
    def check_limb(keypath: str, limb: dict, name: str, blueprint: dict):
        if limb.__class__ is not dict:
            x: str = limb.__class__.__name__
            raise ge[f'Blueprint{name.title()}Error']({
                'title': f'Blueprint{name.title()}DefineError',
                'keypath': keypath,
                'msg': f'"{name}" type must be a "dict", not "{x}".',
                name: limb
            })

        notdefine = [x for x in ('option', 'env', 'coerce', 'enum', 'set') if blueprint.get(x)]
        if notdefine:
            raise ge.BlueprintLimbError({
                'title': '',
                'keypath': keypath,
                'msg': f'''Limb can't define {notdefine}.'''
            })

    def verify_type(self, keypath: str, key: str, value, blueprint: dict, *, full_value: tuple = None):
        if value.__class__ in (tuple, list) and not full_value:
            blueprint[key] = tuple(self.verify_type(
                keypath, key, v, blueprint, full_value=value) for v in value)
        else:
            try:
                value = types[value]
            except (KeyError, TypeError):
                value = full_value.__class__(getattr(x, '__name__', x) for x in full_value) \
                    if full_value else getattr(value, '__name__', value)
                raise ge.BlueprintTypeError({
                    'keypath': f'{keypath}.{key}',
                    'value': value,
                    'msg': f'Unsupported type.',
                    'supported_types': types_supported,
                    'hint': 'If you need to define multiple types, use "tuple" or "list".'
                })

            if full_value:
                return value

            blueprint[key] = value

    @staticmethod
    def verify_option(keypath: str, key: str, value: str, blueprint: dict):
        if value.__class__ is not str:
            x: str = value.__class__.__name__
            raise ge.BlueprintOptionError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': f'Option type must be a "str", not "{x}".'
            })
        elif value[:2] == '--':
            shortopts, longopts, name = '', [value[2:] + '='], value[2:]
        elif value[0] == '-':
            shortopts, longopts, name = value[1:] + ':', [], value[1:]
        else:
            raise ge.BlueprintOptionError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'Option must start with "-" or "--".'
            })

        opt = gopt.new()
        opt(shortopts, longopts)
        blueprint[key] = opt.get(name)

    @staticmethod
    def verify_env(keypath: str, key: str, value: str, blueprint: dict):
        if value.__class__ is not str:
            x: str = value.__class__.__name__
            raise ge.BlueprintENVError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': f'ENV type must be a "str", not "{x}".'
            })
        blueprint[key] = os.getenv(value)

    @staticmethod
    def verify_coerce(keypath: str, key: str, value: str, blueprint: dict):
        try:
            value = coerces[value]
        except (KeyError, TypeError):
            raise ge.BlueprintCoerceError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'Unsupported conversion type.',
                'supported_coerces': coerces_supported
            })
        blueprint[key] = value

    @staticmethod
    def verify_enum(keypath: str, key: str, value: tuple, blueprint: dict):
        if value.__class__ not in (tuple, list):
            x: str = value.__class__.__name__
            raise ge.BlueprintEnumError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': f'Enum type must be a "tuple" or "list", not "{x}".'
            })
        blueprint[key] = tuple(set(value))

    @staticmethod
    def verify_set(keypath: str, key: str, value: tuple, blueprint: dict):
        if value.__class__ not in (tuple, list):
            x: str = value.__class__.__name__
            raise ge.BlueprintSetError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': f'Set type must be a "tuple" or "list", not "{x}".'
            })
        if len(value) < 2:
            raise ge.BlueprintSetError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'Set length must be greater than 1.'
            })
        blueprint[key] = tuple(set(value))

    def verify_verify(self, keypath: str, key: str, value, blueprint: dict, *, full_value=None):
        value_type = value.__class__
        if value_type in (tuple, list) and not full_value:
            blueprint[key] = value_type(self.verify_verify(
                keypath, key, v, blueprint, full_value=value) for v in value)
        else:
            if value.__class__ is str:
                raw_value = value
                try:
                    path, _, func = value.rpartition('.')
                    value = gimport(path, func)
                    if not callable(value):
                        raise ge.BlueprintVerifyError({
                            'keypath': keypath,
                            'value': full_value or raw_value,
                            'msg': "It's not callable."
                        })
                except (ModuleNotFoundError, AttributeError) as e:
                    if re.fullmatch(r'[a-zA-Z_][\w.]+?', value):
                        raise ge.BlueprintVerifyError({
                            'keypath': f'{keypath}.{key}',
                            'value': full_value or value,
                            'msg': e
                        })
                    value = re.compile(value)
            elif value.__class__ is not re.Pattern and not callable(value):
                raise ge.BlueprintVerifyError({
                    'keypath': f'{keypath}.{key}',
                    'value': full_value or value,
                    'msg': 'Unsupported verify.',
                    'supported_verify': ['Regular Expression', 're.Pattern object',
                                         'callable object', 'callable object path'],
                    'hint': 'If you need to define multiple verify, use "tuple" or "list", '
                            '"tuple" will be execute in "and" mode, '
                            '"list" will be execute in "or" mode.',
                })
            if full_value:
                return value
            blueprint[key] = value

    @staticmethod
    def verify_callback(keypath: str, key: str, value, blueprint: dict):
        if value.__class__ is str:
            try:
                path, _, func = value.rpartition('.')
                value = gimport(path, func)
            except (ModuleNotFoundError, AttributeError) as e:
                raise ge.BlueprintCallbackError({
                    'keypath': keypath,
                    'value': value,
                    'msg': e
                })
        if not callable(value):
            raise ge.BlueprintCallbackError({
                'keypath': keypath,
                'value': value,
                'msg': 'Not a callable function.'
            })
        blueprint[key] = value


class DataValidator:

    def __init__(self, data: dict, blueprint: DataBlueprint):
        self.blueprint = blueprint

        if not isinstance(data, dict):
            x: str = data.__class__.__name__
            raise ge.DataTypeError(f'Data type must be a "dict", not "{x}".')

        self.data = data

    def verify(self, *, else_raise: bool = False) -> (dict, None):
        for key, sub_blueprint in self.blueprint:
            err: dict = self.decompose(
                keypath=key,
                blueprint=sub_blueprint,
                value=self.data.get(key, unique),
                data=self.data,
                key=key
            )
            if err:
                if else_raise:
                    raise ge[err.pop('title')](err)
                return err

    def decompose(self, keypath: str, blueprint: dict, value, data, key):
        branch, items = blueprint.get('branch'), blueprint.get('items')

        code, value = self.begin_verify(keypath, blueprint, value, data, key)
        if not code:
            return value

        if branch:
            for key, sub_blueprint in branch.items():
                err: dict = self.decompose(f'{keypath}.{key}', sub_blueprint, value.get(key, unique), value, key)
                if err:
                    return err
        elif items:
            for index, item in enumerate(value):
                err: dict = self.decompose(f'{keypath}[{index}]', items, item, value, index)
                if err:
                    return err

    def begin_verify(self, keypath: str, blueprint: dict, value, data, key):
        option, env = blueprint.get('option'), blueprint.get('env')

        # if value == unique:
        #     if 'default' not in blueprint:
        #         return 0, {
        #             'title': 'DataNotFoundError',
        #             'keypath': keypath,
        #             'msg': 'Data not found.'
        #         }
        #     value = data[key] = blueprint['default']
        #
        # if env:
        #     code, value = self.verify_env(keypath, blueprint['env'], value, data, key)
        #     if not code:
        #         return 0, value
        #
        # if option:
        #     code, value = self.verify_option(keypath, blueprint['option'], value, data, key)
        #     if not code:
        #         return 0, value

        if option:
            code, value = self.verify_option(keypath, blueprint['option'], value, data, key)
            if not code:
                return 0, value
        elif env:
            code, value = self.verify_env(keypath, blueprint['env'], value, data, key)
            if not code:
                return 0, value
        elif value == unique:
            if 'default' not in blueprint:
                return 0, {
                    'title': 'DataNotFoundError',
                    'keypath': keypath,
                    'msg': 'Data not found.'
                }
            value = data[key] = blueprint['default']

        for name in 'type', 'coerce', 'enum', 'set', 'verify', 'callback':
            try:
                x = blueprint[name]
            except KeyError:
                continue
            if x:
                code, value = getattr(self, f'verify_{name}')(keypath, x, value, data, key)
                if not code:
                    return 0, value

        return 1, value

    @staticmethod
    def verify_option(_, option: str, value, data, key) -> tuple:
        if option is not None:
            value = data[key] = option
        return 1, value

    @staticmethod
    def verify_env(_, env: str, value, data, key) -> tuple:
        if env is not None:
            value = data[key] = env
        return 1, value

    @staticmethod
    def verify_type(keypath: str, type_: type, value, _, __) -> tuple:
        if not isinstance(value, type_):
            x, y = type_.__name__, value.__class__.__name__
            return 0, {
                'title': 'DataTypeError',
                'keypath': keypath,
                'value': value,
                'type': x,
                'msg': f'Data type must be "{x}", not "{y}".'
            }
        return 1, value

    @staticmethod
    def verify_coerce(keypath: str, coerce: type, value, data, key) -> tuple:
        if value.__class__ is not coerce:
            try:
                value = data[key] = coerce(value)
            except (TypeError, ValueError) as e:
                return 0, {
                    'title': 'DataCoerceError',
                    'keypath': keypath,
                    'value': value,
                    'coerce': coerce.__name__,
                    'msg': e
                }
        return 1, value

    @staticmethod
    def verify_enum(keypath: str, enum: tuple, value, _, __) -> tuple:
        if value not in enum:
            return 0, {
                'title': 'DataEnumError',
                'keypath': keypath,
                'value': value,
                'enum': enum,
                'msg': 'Value not in enum.'
            }
        return 1, value

    @staticmethod
    def verify_set(keypath: str, set_: tuple, value, data, key) -> tuple:
        if value.__class__ in (list, tuple):
            notfound = [x for x in value if x not in set_]
            if notfound:
                return 0, {
                    'title': 'DataSetError',
                    'keypath': keypath,
                    'value': value,
                    'set': set_,
                    'msg': f'{notfound} not in set.'
                }
        else:
            if value not in set_:
                return 0, {
                    'title': 'DataSetError',
                    'keypath': keypath,
                    'value': value,
                    'set': set_,
                    'msg': 'Value not in set.'
                }
            value = data[key] = [value]
        return 1, value

    def verify_verify(self, keypath: str, verify, value, _, __, *, full_verify=None) -> tuple:
        if verify.__class__ in (list, tuple):
            func = any if verify.__class__ is list else all
            results = [self.verify_verify(keypath, v, value, _, __, full_verify=verify) for v in verify]
            if not func(x[0] for x in results):
                return 0, {
                    'title': 'DataVerifyError',
                    'keypath': keypath,
                    'value': value,
                    'verify': verify,
                    'msg': 'Verify failed.',
                    'hint': '"tuple" will be execute in "and" mode, '
                            '"list" will be execute in "or" mode.'
                }
        elif verify.__class__ is re.Pattern:
            if not verify.fullmatch(value):
                return 0, {
                    'title': 'DataVerifyError',
                    'keypath': keypath,
                    'value': value,
                    'verify': full_verify or verify,
                    'msg': 'Value does not match the validation regex.'
                }
        else:
            if not verify(value):
                return 0, {
                    'title': 'DataVerifyError',
                    'keypath': keypath,
                    'value': value,
                    'verify': full_verify or verify,
                    'msg': 'Value verification failed.'
                }
        return 1, value

    @staticmethod
    def verify_callback(_, callback, value, data, key) -> tuple:
        value = data[key] = callback(value)
        return 1, value
