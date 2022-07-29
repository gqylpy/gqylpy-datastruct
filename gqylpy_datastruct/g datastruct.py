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

Copyright (c) 2022 GQYLPY <http://gqylpy.com>. All rights reserved.

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
import sys
import inspect
import datetime as dt

import gqylpy_exception as ge

from typing import Union, Callable, NoReturn, Any

unique = b'GQYLPY, \xe6\x94\xb9\xe5\x8f\x98\xe4\xb8\x96\xe7\x95\x8c\xe3\x80\x82'

coerces_supported = int, float, str, bytes, list, tuple, set, dict, bool
types_supported = coerces_supported + (type(None), dt.date, dt.time, dt.datetime)

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


class DataStruct:

    def __init__(self, blueprint: dict):
        if blueprint.__class__ is not dict:
            x: str = blueprint.__class__.__name__
            raise ge.BlueprintStructureError(
                f'Blueprint type must be a "dict", not "{x}".'
            )

        for key, sub_blueprint in blueprint.items():
            self.disassemble(key, sub_blueprint, blueprint, key)

        self.blueprint = blueprint

    def verify(self, data: dict, *, eraise: bool = False) -> Union[dict, None]:
        return DataValidator(data, self.blueprint).verify(eraise=eraise)

    def disassemble(
            self,
            keypath:       str,
            blueprint:     dict,
            sup_blueprint: dict,
            sup_key:       str
    ):
        if blueprint.__class__ is not dict:
            if blueprint in (None, ...):
                sup_blueprint[sup_key] = {}
                return
            x: str = blueprint.__class__.__name__
            raise ge.BlueprintStructureError({
                'keypath': keypath,
                'msg': f'Blueprint structure must be defined using "dict", not "{x}".'
            })

        for keywork_special in (type, set):
            if keywork_special in blueprint:
                blueprint[keywork_special.__name__] = blueprint.pop(keywork_special)

        for key, value in blueprint.items():
            if not(key in ('branch', 'items', 'default') or value in (None, ..., '')):
                if blueprint.get('option') and blueprint.get('option_bool'):
                    raise ge.BlueprintStructureError({
                        'keypath': keypath,
                        'msg': 'Verification method "option" and '
                               '"option_bool" cannot exist together.'
                    })
                try:
                    verify_func: Callable = getattr(self, f'verify_{key}')
                except AttributeError:
                    raise ge.BlueprintVerifyMethodError({
                        'keypath': keypath,
                        'verify_method': key,
                        'msg': f'Unsupported verification method "{key}".',
                        'supported_verify_method': verify_method_supported
                    })
                verify_func(keypath, key, value, blueprint)

        branch: dict = self.get_limb_and_verify(keypath, blueprint, 'branch')
        items: dict = self.get_limb_and_verify(keypath, blueprint, 'items')

        if branch and items:
            raise ge.BlueprintStructureError({
                'keypath': keypath,
                'msg': '"branch" and "items" cannot exist together.'
            })

        if branch:
            for key, sub_blueprint in branch.items():
                self.disassemble(f'{keypath}.branch.{key}', sub_blueprint, branch, key)
        elif items:
            self.disassemble(f'{keypath}.items', items, items, sup_key)

    @staticmethod
    def get_limb_and_verify(
            keypath:   str,
            blueprint: dict,
            limbtype:  str
    ) -> Union[dict, None]:
        try:
            limb: dict = blueprint[limbtype]
        except KeyError:
            return

        if limb in ({}, None, ...):
            del blueprint[limbtype]
            return

        if limb.__class__ is not dict:
            x: str = limb.__class__.__name__
            raise ge.BlueprintStructureError({
                'title': f'Blueprint{limbtype.title()}DefineError',
                'keypath': keypath,
                'msg': f'"{limbtype}" type must be a "dict", not "{x}".',
                limbtype: limb
            })

        notdefine = [x for x in (
            'option', 'option_bool', 'env', 'coerce', 'enum', 'set'
        ) if blueprint.get(x)]

        if notdefine:
            x: str = f'"{notdefine[0]}"' if len(notdefine) == 1 else notdefine
            raise ge.BlueprintStructureError({
                'keypath': keypath,
                'msg': f'Limb can not define {x}.'
            })

        return limb

    def verify_type(
            self,
            keypath:    str,
            key:        str,
            value:      Union[type, str, tuple, list],
            blueprint:  dict,
            *,
            full_value: Union[tuple, list] = None
    ):
        if value.__class__ in (tuple, list) and not full_value:
            if value.__class__ is tuple:
                value: list = list(value)
            delete_repeated(value)
            blueprint[key] = tuple(self.verify_type(
                keypath, key, v, blueprint, full_value=value
            ) for v in value)
        else:
            if value.__class__ is str:
                value: str = value.strip()
            try:
                value: type = types[value]
            except (KeyError, TypeError):
                value: str = getattr(value, '__name__', value)
                full_value: Union[str, tuple, list] = full_value.__class__(
                    getattr(x, '__name__', x) for x in full_value
                ) if full_value else value
                raise ge.BlueprintTypeError({
                    'keypath': f'{keypath}.{key}',
                    'value': full_value,
                    'msg': f'Unsupported type "{value}".',
                    'supported_types': types_supported,
                    'hint': 'If you need to define multiple types, use "tuple" or "list".'
                })

            if full_value:
                return value

            blueprint[key] = value

    def verify_option(
            self,
            keypath:    str,
            key:        str,
            value:      Union[str, tuple, list],
            blueprint:  dict,
            *,
            full_value: Union[tuple, list]      = None,
            boole:      bool                    = False
    ):
        if value.__class__ in (tuple, list) and not full_value:
            for v in value:
                self.verify_option(
                    keypath, key, v, blueprint, full_value=value, boole=boole
                )
        elif value.__class__ is str:
            value: str = value.strip()
        else:
            x: str = value.__class__.__name__
            raise ge[f'BlueprintOption{"Bool" if boole else ""}Error']({
                'keypath': f'{keypath}.{key}',
                'value': full_value or value,
                'msg': f'Option type must be a "str", not "{x}".',
                'hint': 'If you need to define multiple options, use "tuple" or "list".'
            })
        if not full_value:
            blueprint[key] = getopt(
                *[value] if value.__class__ is str else value,
                boole=boole
            )

    def verify_option_bool(
            self,
            keypath:   str,
            key:       str,
            value:     Union[str, tuple, list],
            blueprint: dict
    ):
        self.verify_option(keypath, key, value, blueprint, boole=True)

    @staticmethod
    def verify_env(
            keypath:   str,
            key:       str,
            value:     str,
            blueprint: dict
    ):
        if value.__class__ is not str:
            x: str = value.__class__.__name__
            raise ge.BlueprintENVError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': f'The "env" type must be a "str", not "{x}".'
            })
        blueprint[key] = os.getenv(value)

    @staticmethod
    def verify_coerce(
            keypath:   str,
            key:       str,
            value:     Union[str, type],
            blueprint: dict
    ):
        if value.__class__ is str:
            value: str = value.strip()
        try:
            value: type = coerces[value]
        except (KeyError, TypeError):
            raise ge.BlueprintCoerceError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'Unsupported conversion type.',
                'supported_coerces': coerces_supported
            })
        blueprint[key] = value

    @staticmethod
    def verify_enum(
            keypath:   str,
            key:       str,
            value:     Union[tuple, list],
            blueprint: dict
    ):
        if value.__class__ is tuple:
            value = list(value)
        elif value.__class__ is not list:
            x: str = value.__class__.__name__
            raise ge.BlueprintEnumError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': f'The "enum" type must be a "tuple" or "list", not "{x}".'
            })
        delete_repeated(value)
        blueprint[key] = tuple(value)

    @staticmethod
    def verify_set(
            keypath:   str,
            key:       str,
            value:     Union[tuple, list],
            blueprint: dict
    ):
        if value.__class__ is tuple:
            value = list(value)
        elif value.__class__ is not list:
            x: str = value.__class__.__name__
            raise ge.BlueprintSetError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': f'The "set" type must be a "tuple" or "list", not "{x}".'
            })
        if len(value) < 2:
            raise ge.BlueprintSetError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'The "set" length must be greater than 1.'
            })

        delete_repeated(value)
        blueprint[key] = value

    def verify_verify(
            self,
            keypath:    str,
            key:        str,
            value:      Union[str, Callable, re.Pattern, tuple, list],
            blueprint:  dict,
            *,
            full_value: Union[tuple, list] = None
    ):
        value_type: type = value.__class__

        if value_type in (tuple, list) and not full_value:
            blueprint[key] = value_type(self.verify_verify(
                keypath, key, v, blueprint, full_value=value
            ) for v in value)
        else:
            if value.__class__ is str:
                raw_value: str = value
                try:
                    path, _, func = value.rpartition('.')
                    value: Callable = gimport(path, func)
                    if not (callable(value) and inspect.signature(value).parameters):
                        raise ge.BlueprintVerifyError({
                            'keypath': keypath,
                            'value': full_value or raw_value,
                            'msg': 'Verification function must be callable '
                                   'and take at least one parameter.'
                        })
                except (ModuleNotFoundError, AttributeError, ValueError) as e:
                    if re.fullmatch(r'[a-zA-Z_][\w.]+?', value):
                        raise ge.BlueprintVerifyError({
                            'keypath': f'{keypath}.{key}',
                            'value': full_value or value,
                            'msg': str(e)
                        })
                    value: re.Pattern = re.compile(value)
            elif callable(value):
                if not inspect.signature(value).parameters:
                    raise ge.BlueprintVerifyError({
                        'keypath': keypath,
                        'value': full_value or value,
                        'msg': 'Verification function must take at least one parameter.'
                    })
            elif value.__class__ is not re.Pattern:
                raise ge.BlueprintVerifyError({
                    'keypath': f'{keypath}.{key}',
                    'value': full_value or value,
                    'msg': 'Unsupported verify mode.',
                    'supported_verify_mode': [
                        'Regular Expression', 're.Pattern object',
                        'callable object', 'callable object path'
                    ],
                    'hint': 'If you need to define multiple verify, use "tuple" or "list", '
                            '"tuple" will be execute in "and" mode, '
                            '"list" will be execute in "or" mode.',
                })

            if full_value:
                return value

            blueprint[key] = value

    @staticmethod
    def verify_callback(
            keypath:   str,
            key:       str,
            value:     Union[Callable, str],
            blueprint: dict
    ):
        if value.__class__ is str:
            try:
                path, _, func = value.rpartition('.')
                value: Callable = gimport(path, func)
            except (ModuleNotFoundError, AttributeError, ValueError) as e:
                raise ge.BlueprintCallbackError({
                    'keypath': keypath,
                    'value': value,
                    'msg': str(e)
                })
        if not callable(value):
            raise ge.BlueprintCallbackError({
                'keypath': keypath,
                'value': value,
                'msg': 'Not a callable object.'
            })
        blueprint[key] = value


class DataValidator:

    def __init__(self, data: dict, blueprint: dict):
        if not isinstance(data, dict):
            x: str = data.__class__.__name__
            raise ge.DataStructureError(
                f'Data type must be a "dict", not "{x}".'
            )
        self.data = data
        self.blueprint = blueprint

    def verify(self, *, eraise: bool = False) -> Union[dict, None]:
        for key, sub_blueprint in self.blueprint.items():
            err: dict = self.disassemble(
                keypath=key,
                blueprint=sub_blueprint,
                value=self.data.get(key, unique),
                data=self.data,
                key=key
            )
            if err:
                if eraise:
                    raise ge[err.pop('title')](err)
                return err

    def disassemble(
            self,
            keypath:   str,
            blueprint: dict,
            value:     Any,
            data:      Union[dict, list],
            key:       Union[str, int]
    ) -> Union[dict, None]:
        option:      str  = blueprint.get('option')
        option_bool: bool = blueprint.get('option_bool')
        env:         str  = blueprint.get('env')

        if option:
            value: str = self.verify_option(option, data, key)
        elif option_bool or option_bool is False:
            value: bool = self.verify_option_bool(option_bool, data, key)
        elif env:
            value: str = self.verify_env(env, data, key)
        elif value is unique:
            if 'default' not in blueprint:
                return {
                    'title': 'DataNotFoundError',
                    'keypath': keypath,
                    'msg': 'Data not found.'
                }
            value = data[key] = blueprint['default']

        for name in 'type', 'coerce', 'enum', 'set', 'verify', 'callback':
            try:
                x: Any = blueprint[name]
            except KeyError:
                continue
            if x not in (None, ..., ''):
                code, value = getattr(self, f'verify_{name}')(
                    keypath, x, value, data, key
                )
                if not code:
                    return value

        branch: dict = blueprint.get('branch')
        items:  dict = blueprint.get('items')

        if branch:
            for key, sub_blueprint in branch.items():
                err: dict = self.disassemble(
                    f'{keypath}.{key}', sub_blueprint,
                    value.get(key, unique), value, key
                )
                if err:
                    return err
        elif items:
            for index, item in enumerate(value):
                err: dict = self.disassemble(
                    f'{keypath}[{index}]', items, item, value, index
                )
                if err:
                    return err

    @staticmethod
    def verify_option(option: str, data: dict, key: str) -> str:
        value = data[key] = option
        return value

    @staticmethod
    def verify_option_bool(option: bool, data: dict, key: str) -> bool:
        value = data[key] = option
        return value

    @staticmethod
    def verify_env(env: str, data: dict, key: str) -> str:
        value = data[key] = env
        return value

    @staticmethod
    def verify_type(
            keypath: str,
            type_:   Union[type, tuple],
            value:   Any,
            _, __
    ) -> tuple:
        if not isinstance(value, type_):
            if type_.__class__ in (tuple, list):
                type_ = type_.__class__(t.__name__ for t in type_)
                msg = f'in [{", ".join(type_)}]'
            else:
                type_: str = type_.__name__
                msg = f'a "{type_}"'
            x = value.__class__.__name__
            return 0, {
                'title': 'DataTypeError',
                'keypath': keypath,
                'value': value,
                'type': type_,
                'msg': f'Data type must be {msg}, not "{x}".'
            }
        return 1, value

    @staticmethod
    def verify_coerce(
            keypath: str,
            coerce:  type,
            value:   Any,
            data:    dict,
            key:     str
    ) -> tuple:
        if value.__class__ is not coerce:
            try:
                value = data[key] = coerce(value)
            except (TypeError, ValueError) as e:
                return 0, {
                    'title': 'DataCoerceError',
                    'keypath': keypath,
                    'value': value,
                    'coerce': coerce.__name__,
                    'msg': str(e)
                }
        return 1, value

    @staticmethod
    def verify_enum(
            keypath: str,
            enum:    Union[tuple, list],
            value:   Any,
            _, __
    ) -> tuple:
        if value not in enum:
            return 0, {
                'title': 'DataEnumError',
                'keypath': keypath,
                'value': value,
                'enum': enum,
                'msg': f'"{value}" is not in enum.'
            }
        return 1, value

    @staticmethod
    def verify_set(
            keypath: str,
            set_:    Union[tuple, list],
            value:   Any,
            data:    dict,
            key:     str
    ) -> tuple:
        if value.__class__ in (list, tuple):
            notfound = [x for x in value if x not in set_]
            if notfound:
                x: Any = notfound[0] if len(notfound) == 1 \
                    else ','.join(notfound)
                return 0, {
                    'title': 'DataSetError',
                    'keypath': keypath,
                    'value': value,
                    'set': set_,
                    'msg': f'There is no "{x}" in set.'
                }
        else:
            if value not in set_:
                return 0, {
                    'title': 'DataSetError',
                    'keypath': keypath,
                    'value': value,
                    'set': set_,
                    'msg': f'"{value}" is not in set.'
                }
            value = data[key] = [value]
        return 1, value

    def verify_verify(
            self,
            keypath:     str,
            verify:      Union[re.Pattern, Callable, list, tuple],
            value:       Any,
            _, __,
            *,
            full_verify: Union[list, tuple] = None
    ) -> tuple:
        if verify.__class__ in (list, tuple):
            mode = any if verify.__class__ is list else all
            results = [self.verify_verify(
                keypath, v, value, _, __, full_verify=verify
            ) for v in verify]
            if not mode(x[0] for x in results):
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
            if value.__class__ in (int, float):
                value = str(value)
            try:
                result = verify.search(value)
            except TypeError as e:
                return 0, {
                    'title': 'DataVerifyError',
                    'keypath': keypath,
                    'value': value,
                    'verify': full_verify or verify.pattern,
                    'msg': str(e)
                }
            if not result:
                return 0, {
                    'title': 'DataVerifyError',
                    'keypath': keypath,
                    'value': value,
                    'verify': full_verify or verify.pattern,
                    'msg': f'Value "{value}" does not match the '
                           f'validation regular "{verify.pattern}".'
                }
        elif not verify(value):
            return 0, {
                'title': 'DataVerifyError',
                'keypath': keypath,
                'value': value,
                'verify': full_verify or verify,
                'msg': 'Value verification failed.'
            }
        return 1, value

    @staticmethod
    def verify_callback(
            _,
            callback: Callable,
            value:    Any,
            data:     Union[dict, list],
            key:      Union[str, int]
    ) -> tuple:
        value = data[key] = callback(value)
        return 1, value


def delete_repeated(data: list):
    index = len(data) - 1
    while index > -1:
        offset = -1
        while index + offset > -1:
            if data[index + offset] == data[index]:
                del data[index]
                break
            else:
                offset -= 1
        index -= 1


def getopt(*options, boole: bool = False) -> Union[str, bool, NoReturn]:
    args:  list = sys.argv[1:]
    index: int  = len(args) - 1

    while index > -1:
        value: str = args[index]

        if value in options:
            if boole:
                return True
            if index + 1 < len(args) and args[index + 1][0] != '-':
                return args[index + 1]
            raise ge.OptionError(f'Option "{value}" need a parameter.')

        for opt in options:
            if value.startswith(opt + '='):
                if boole:
                    x: str = value.split("=", 1)[0]
                    raise ge.OptionError(
                        f'''Option "{x}" don't need parameter.''')
                return value.split('=', 1)[1]

        index -= 1

    if boole:
        return False


def gimport(path: str, attr: str = None, *, define=None) -> Any:
    try:
        __import__(path)
        module_ = sys.modules[path]
        return getattr(module_, attr) if attr else module_
    except (ValueError, ModuleNotFoundError, AttributeError) as e:
        if define is not None:
            return define
        raise e


verify_method_supported = [
    x[7:] for x in dir(DataStruct) if x[:7] == 'verify_'
]
