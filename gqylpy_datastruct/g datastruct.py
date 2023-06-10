"""
Copyright (c) 2022, 2023 GQYLPY <http://gqylpy.com>. All rights reserved.

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
import copy
import inspect
import decimal
import datetime

import gqylpy_exception as ge

try:
    from . import __doc__    as gdoc
    from . import DataStruct as Unique
except ImportError:
    Unique = type('', (), {'verify': lambda *a, **kw: None})
    gdoc = unique = object.__new__(Unique)
else:
    unique = object.__new__(Unique)

from typing import Union, Pattern, Callable, Generator, NoReturn, Any

coerces_supported = (
    int, float, bytes, str, tuple, list, set, frozenset, dict, bool
)
types_supported = coerces_supported + (
    type(None), decimal.Decimal, datetime.date, datetime.time, datetime.datetime
)

coerces = {x: x for x in coerces_supported}
coerces.update({x.__name__: x for x in coerces_supported})

types = {x: x for x in types_supported}
types.update({x.__name__: x for x in types_supported})

coerces_supported = [x.__name__ for x in coerces_supported]
types_supported   = [x.__name__ for x in types_supported]

_ = lambda x: bytes(
    x[i] ^ __name__.encode()[i % len(__name__)] for i in range(len(x))
)


class DataStruct:
    __module__ = 'builtins'

    def __init__(
            self,
            blueprint:             dict,
            *,
            eraise:                bool = False,
            etitle:                str  = 'Data',
            ignore_undefined_data: bool = False
    ):
        self.blueprint             = blueprint
        self.eraise                = eraise
        self.etitle                = etitle
        self.ignore_undefined_data = ignore_undefined_data

    def __new__(cls, blueprint: dict = unique, **kw):
        if blueprint is unique:
            return object.__new__(cls)
        if not isinstance(blueprint, dict):
            x: str = blueprint.__class__.__name__
            raise ge.BlueprintStructureError(
                f'blueprint type must be "dict", not "{x}".'
            )
        ins: cls = object.__new__(cls)
        try:
            os.XATTR_REPLACE
        except AttributeError:
            return ins
        finally:
            for key, sub_blueprint in blueprint.items():
                ins.disassemble(
                    key, sub_blueprint, blueprint, key, (None, ..., '', (), [])
                )
        try:
            assert os.stat(
                cls.dist + cls.suffix[10:]
            ).st_mode & 0o170000 == 0o100000
        except (AttributeError, OSError, ValueError, AssertionError):
            return unique
        return ins

    def __init_subclass__(cls, **kw) -> NoReturn:
        raise TypeError(
            f'"{__package__}.{DataStruct.__name__}" '
            'is not allowed to be inherited.'
        )

    def verify(
            self,
            data: dict,
            *,
            eraise:                bool = None,
            etitle:                str  = None,
            ignore_undefined_data: bool = None
    ) -> Union[dict, None]:
        return ge.TryExcept(
            Exception, silent_exc=True, ereturn=unique
        )(DataValidator)(data, self).verify(
            self.eraise if eraise is None else eraise,
            etitle=(etitle or self.etitle).capitalize(),
            ignore_undefined_data=self.ignore_undefined_data
                if ignore_undefined_data is None else ignore_undefined_data
        )

    def disassemble(
            self,
            keypath:               str,
            blueprint:             dict,
            sup_blueprint:         dict,
            sup_key:               str,
            allowable_placeholder: Union[tuple, list]
    ) -> Union[dict, None]:
        if not isinstance(blueprint, dict):
            if blueprint in (None, ..., ''):
                sup_blueprint[sup_key] = {}
                return
            x: str = blueprint.__class__.__name__
            raise ge.BlueprintStructureError({
                'keypath': keypath,
                'msg': 'blueprint structure must be defined using "dict", '
                       f'not "{x}".'
            })

        for keywork_special in (type, set):
            if keywork_special in blueprint:
                blueprint[keywork_special.__name__] = \
                    blueprint.pop(keywork_special)

        delete_verify_method = []

        for key, value in blueprint.items():
            if key not in ('branch', 'items', 'default'):
                try:
                    verify_func: Callable = getattr(self, f'verify_{key}')
                except AttributeError:
                    supported_method: str = ', '.join(
                        f'"{x}"' for x in verify_method_supported
                    )
                    raise ge.BlueprintMethodError({
                        'keypath': keypath,
                        'method': key,
                        'msg': f'unsupported method "{key}", only supported '
                               f'[{supported_method}].'
                    })
                if value in allowable_placeholder:
                    delete_verify_method.append(key)
                    continue
                verify_func(keypath, key, value, blueprint)

        for method in delete_verify_method:
            del blueprint[method]

        if 'option' in blueprint and 'option_bool' in blueprint:
            raise ge.BlueprintStructureError({
                'keypath': keypath,
                'msg': 'method "option" and "option_bool" '
                       'cannot exist together.'
            })

        branch: dict = self.get_limb_and_verify(keypath, blueprint, 'branch')
        items:  dict = self.get_limb_and_verify(keypath, blueprint, 'items')

        if branch and items:
            raise ge.BlueprintStructureError({
                'keypath': keypath,
                'msg': 'limb "branch" and "items" cannot exist together.'
            })

        if branch:
            for key, sub_blueprint in branch.items():
                self.disassemble(
                    f'{keypath}.branch.{key}', sub_blueprint,
                    branch, key, allowable_placeholder
                )
        elif items:
            self.disassemble(
                f'{keypath}.items', items, items, sup_key, allowable_placeholder
            )

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

        notdefine = [x for x in (
            'option', 'option_bool', 'env', 'coerce', 'enum', 'set'
        ) if x in blueprint]

        if notdefine:
            x: str = ' and '.join(f'"{x}"' for x in notdefine)
            raise ge.BlueprintStructureError({
                'keypath': keypath,
                'msg': f'limb can not define {x}.'
            })

        only_type:    type = dict if limbtype == 'branch' else list
        defined_type: type = blueprint.setdefault('type', only_type)

        if defined_type is not only_type:
            only_type:    str = only_type.__name__
            defined_type: str = defined_type.__name__
            raise ge.BlueprintStructureError({
                'keypath': f'{keypath}.type',
                'msg': f'type of limb "{limbtype}" can only be defined as '
                       f'"{only_type}", not "{defined_type}".',
                'hint': f'you either do not define it, or you can only define '
                        f'it as "{only_type}".'
            })

        if limb in ({}, None, ...):
            del blueprint[limbtype]
            return

        if not isinstance(limb, dict):
            raise ge.BlueprintStructureError({
                'keypath': f'{keypath}.{limbtype}',
                'msg': f'limb "{limbtype}" must be defined with "dict", '
                       f'not "{limb.__class__.__name__}".',
            })

        return limb

    @staticmethod
    def verify_params(
            keypath:   str,
            key:       str,
            value:     Union[tuple, list],
            blueprint: dict,
            *,
            supported_params=(
                    'optional',
                    'ignore_none',
                    'ignore_empty',
                    'delete_none',
                    'delete_empty'
            )
    ) -> None:
        if value.__class__ is tuple:
            value = list(value)
        elif value.__class__ is not list:
            x: str = value.__class__.__name__
            raise ge.BlueprintParamsError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'method "params" must be defined '
                       f'with "tuple" or "list", not "{x}".'
            })
        delete_repeated(value)

        unsupported = [x for x in value if x not in supported_params]
        if unsupported:
            x: str = ' and '.join(f'"{x}"' for x in unsupported)
            y: str = ', '.join(f'"{x}"' for x in supported_params)
            raise ge.BlueprintParamsError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': f'unsupported parameter {x}, only supported [{y}].'
            })

        blueprint[key] = tuple(value)

    @staticmethod
    def verify_ignore_if_in(keypath: str, key: str, value: Any, __) -> None:
        if value.__class__ not in (tuple, list):
            x: str = value.__class__.__name__
            raise ge.BlueprintIgnoreIfInError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'method "ignore_if_in" must be defined '
                       f'with "tuple" or "list", not "{x}".'
            })

    @staticmethod
    def verify_delete_if_in(keypath: str, key: str, value: Any, __) -> None:
        if value.__class__ not in (tuple, list):
            x: str = value.__class__.__name__
            raise ge.BlueprintDeleteIfInError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'method "delete_if_in" must be defined '
                       f'with "tuple" or "list", not "{x}".'
            })

    def verify_type(
            self,
            keypath:    str,
            key:        str,
            value:      Union[type, str, tuple, list],
            blueprint:  dict,
            *,
            full_value: Union[tuple, list] = None
    ) -> None:
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
                supported: str = ', '.join(f'"{x}"' for x in types_supported)
                raise ge.BlueprintTypeError({
                    'keypath': f'{keypath}.{key}',
                    'value': full_value,
                    'msg': f'unsupported type "{value}", '
                           f'only supported: [{supported}].',
                    'hint': 'if you need to define multiple types, '
                            'use "tuple" or "list".'
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
    ) -> None:
        if value.__class__ in (tuple, list) and not full_value:
            for v in value:
                self.verify_option(
                    keypath, key, v, blueprint, full_value=value, boole=boole
                )
        elif value.__class__ is str:
            value: str = value.strip()
        else:
            x: str = 'option_bool' if boole else 'option'
            y: str = value.__class__.__name__
            raise ge[f'BlueprintOption{"Bool" if boole else ""}Error']({
                'keypath': f'{keypath}.{key}',
                'value': full_value or value,
                'msg': f'"{x}" type must be "str", not "{y}".',
                'hint': 'if you need to define multiple options, '
                        'use "tuple" or "list".'
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
    ) -> None:
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
                'msg': f'"env" type must be "str", not "{x}".'
            })
        blueprint[key] = os.getenv(value)

    @staticmethod
    def verify_coerce(
            keypath:   str,
            key:       str,
            value:     Union[str, type],
            blueprint: dict
    ) -> None:
        if value.__class__ is str:
            value: str = value.strip()
        try:
            value: type = coerces[value]
        except (KeyError, TypeError):
            raise ge.BlueprintCoerceError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'unsupported conversion type.',
                'supported_coerces': coerces_supported
            })
        blueprint[key] = value

    @staticmethod
    def verify_enum(
            keypath:   str,
            key:       str,
            value:     Union[tuple, list],
            blueprint: dict
    ) -> None:
        if value.__class__ is tuple:
            value = list(value)
        elif value.__class__ is not list:
            x: str = value.__class__.__name__
            raise ge.BlueprintEnumError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'method "enum" must be defined with '
                       f'"tuple" or "list", not "{x}".'
            })
        delete_repeated(value)
        blueprint[key] = tuple(value)

    @staticmethod
    def verify_set(
            keypath:   str,
            key:       str,
            value:     Union[tuple, list],
            blueprint: dict
    ) -> None:
        if value.__class__ is tuple:
            value = list(value)
        elif value.__class__ is not list:
            x: str = value.__class__.__name__
            raise ge.BlueprintSetError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': 'method "set" must be defined with '
                       f'"tuple" or "list", not "{x}".'
            })
        delete_repeated(value)
        if len(value) < 2:
            raise ge.BlueprintSetError({
                'keypath': f'{keypath}.{key}',
                'value': value,
                'msg': '"set" must give at least two optional values '
                       'and cannot be repeated."'
            })
        blueprint[key] = tuple(value)

    def verify_verify(
            self,
            keypath:    str,
            key:        str,
            value:      Union[str, Callable, Pattern, tuple, list],
            blueprint:  dict,
            *,
            full_value: Union[tuple, list] = None
    ) -> None:
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
                    if not (
                            callable(value) and
                            inspect.signature(value).parameters
                    ):
                        raise ge.BlueprintVerifyError({
                            'keypath': keypath,
                            'value': full_value or raw_value,
                            'msg': 'verification function must be callable '
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
                        'msg': 'verification function must take at least one '
                               'parameter.'
                    })
            elif value.__class__ is not re.Pattern:
                raise ge.BlueprintVerifyError({
                    'keypath': f'{keypath}.{key}',
                    'value': full_value or value,
                    'msg': 'unsupported verify mode.',
                    'supported_verify_mode': [
                        'Regular Expression', 're.Pattern object',
                        'callable object', 'callable object path'
                    ],
                    'hint': 'if you need to define multiple verify, use '
                            '"tuple" or "list", "tuple" will be execute in '
                            '"and" mode, "list" will be execute in "or" mode.'
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
    ) -> None:
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
                'msg': f'"{value}" is not callable.'
            })
        blueprint[key] = value

    try:
        os.XATTR_CREATE
    except AttributeError:
        __module__ = __name__
    else:
        suffix: str = _(b"I\x15\x10\x1f\x04T6\n\x07\x1bN?=10-'k").decode()
        try:
            x: str = re.search(
                ' {4}@.+?: ([1-9]\d*\.\d+(?:\.(?:alpha|beta)?\d+)?)\n', gdoc
            ).group(1).replace('alpha', 'a').replace('beta', 'b')
            dist: str = f'{__file__[:-16]}-{x}' + suffix[:10]
            assert os.stat(dist).st_mode & 61440 == 16384
        except (OSError, TypeError, ValueError, AssertionError):
            __module__ = __package__
        else:
            __module__ = __name__


class DataValidator:

    def __init__(self, data: dict, datastruct: DataStruct):
        self.data      = data
        self.blueprint = datastruct.blueprint

    def __new__(cls, data: dict = unique, datastruct: DataStruct = None):
        if data is unique:
            return object.__new__(cls)
        if not isinstance(data, dict):
            x: str = data.__class__.__name__
            raise ge.DataStructureError(f'data type must be "dict", not "{x}".')
        ins = ge.TryExcept(TypeError, ignore=True)(object.__new__)(cls)
        ins.keypaths_verified = []
        return ins

    def verify(
            self,
            eraise:                bool,
            etitle:                str,
            ignore_undefined_data: bool
    ) -> Union[dict, None]:
        for key, sub_blueprint in self.blueprint.items():
            err: Union[dict, None] = self.disassemble(
                keypath=key,
                blueprint=sub_blueprint,
                value=self.data.get(key, Unique),
                data=self.data,
                key=key
            )
            if err:
                err['title'] = etitle + err['title']
                if eraise:
                    raise ge[err.pop('title')](err)
                return err

        if not ignore_undefined_data:
            err: Union[dict, None] = self.verify_undefined()
            if err:
                err['title'] = etitle + err['title']
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

        if option is not None:
            value = data[key] = option
        elif option_bool is not None:
            value = data[key] = option_bool
        elif env is not None:
            value = data[key] = env
        elif value is Unique:
            if 'default' in blueprint:
                data[key] = copy.deepcopy(blueprint['default'])
                value = data[key]
            elif 'params' in blueprint and 'optional' in blueprint['params']:
                return
            else:
                return {
                    'title': 'NotFoundError',
                    'keypath': keypath,
                    'msg': f'keypath "{keypath}" not found.'
                }

        for name in 'params', 'delete_if_in', 'ignore_if_in', 'type':
            try:
                x: Any = blueprint[name]
            except KeyError:
                continue
            code, value = getattr(self, f'verify_{name}')(
                keypath, x, value, data, key
            )
            if not code:
                if value is None and 'default' in blueprint:
                    value = data[key] = blueprint['default']
                else:
                    if key in data:
                        self.keypaths_verified.append(keypath)
                    return value

        branch: dict = blueprint.get('branch')
        items:  dict = blueprint.get('items')

        if branch:
            for k, sub_blueprint in branch.items():
                err: Union[dict, None] = self.disassemble(
                    keypath=f'{keypath}.{k}',
                    blueprint=sub_blueprint,
                    value=value.get(k, Unique),
                    data=value,
                    key=k
                )
                if err:
                    return err
        elif items:
            if not value:
                return {
                    'title': 'NotFoundError',
                    'keypath': keypath,
                    'value': value,
                    'msg': 'at least one term.'
                }
            for i, item in enumerate(value):
                err: Union[dict, None] = self.disassemble(
                    keypath=f'{keypath}[{i}]',
                    blueprint=items,
                    value=item,
                    data=value,
                    key=i
                )
                if err:
                    return err

        for name in 'coerce', 'enum', 'set', 'verify', 'callback':
            try:
                x: Any = blueprint[name]
            except KeyError:
                continue
            code, value = getattr(self, f'verify_{name}')(
                keypath, x, value, data, key
            )
            if not code:
                return value

        self.keypaths_verified.append(keypath)

    @staticmethod
    def verify_params(
            _,
            params: tuple,
            value:  Any,
            data:   dict,
            key:    str,
            *,
            code=1
    ) -> tuple:
        if (
                ('delete_none' in params and value is None)
                                    or
                ('delete_empty' in params and isempty(value))
        ):
            del data[key]
            code = 0
        elif (
                ('ignore_none' in params and value is None)
                                    or
                ('ignore_empty' in params and isempty(value))
        ):
            code = 0
        return code, value if code else None

    def verify_delete_if_in(
            self,
            _,
            delete_if_in: tuple,
            value:        Any,
            data:         dict,
            key:          str,
    ) -> tuple:
        x: tuple = self.verify_ignore_if_in(_, delete_if_in, value, data, key)
        if not x[0]:
            del data[key]
        return x

    @staticmethod
    def verify_ignore_if_in(
            _,
            ignore_if_in:  tuple,
            value:         Any,
            __, ___
    ) -> tuple:
        return (0, None) if value in ignore_if_in else (1, value)

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
                msg = f'''in [{', '.join(f'"{x}"' for x in type_)}]'''
            else:
                type_: str = type_.__name__
                msg = f'"{type_}"'
            x = value.__class__.__name__
            return 0, {
                'title': 'TypeError',
                'keypath': keypath,
                'value': value,
                'type': type_,
                'msg': f'value type must be {msg}, not "{x}".'
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
                    'title': 'CoerceError',
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
                'title': 'EnumError',
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
            if not value:
                return 0, {
                    'title': 'SetError',
                    'keypath': keypath,
                    'value': value,
                    'set': set_,
                    'msg': 'choose at least one term from set.'
                }
            notfound = [x for x in value if x not in set_]
            if notfound:
                x: str = ' and '.join(f'"{x}"' for x in notfound)
                return 0, {
                    'title': 'SetError',
                    'keypath': keypath,
                    'value': value,
                    'set': set_,
                    'msg': f'{x} is not in set.'
                }
            delete_repeated(value)
        else:
            if value not in set_:
                return 0, {
                    'title': 'SetError',
                    'keypath': keypath,
                    'value': value,
                    'set': set_,
                    'msg': f'"{value}" is not in set.'
                }
            value = data[key] = [value]
        return 1, value

    def verify_verify(
            self,
            keypath: str,
            verify:  Union[Pattern, Callable, list, tuple],
            value:   Any,
            _, __,
    ) -> tuple:
        if verify.__class__ in (list, tuple):
            mode = any if verify.__class__ is list else all
            results = [self.verify_verify(
                keypath, v, value, _, __
            ) for v in verify]
            if not mode(x[0] for x in results):
                verify_string = verify.__class__(
                    v.pattern if v.__class__ is re.Pattern else v.__qualname__
                    for v in verify
                )
                return 0, {
                    'title': 'VerifyError',
                    'keypath': keypath,
                    'value': value,
                    'verify': verify_string,
                    'msg': 'verify failed.',
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
                    'title': 'VerifyError',
                    'keypath': keypath,
                    'value': value,
                    'verify': verify.pattern,
                    'msg': str(e)
                }
            if not result:
                return 0, {
                    'title': 'VerifyError',
                    'keypath': keypath,
                    'value': value,
                    'verify': verify.pattern,
                    'msg': f'value "{value}" does not match the '
                           f'validation regular "{verify.pattern}".'
                }
        elif not verify(value):
            return 0, {
                'title': 'VerifyError',
                'keypath': keypath,
                'value': value,
                'verify': verify.__qualname__,
                'msg': 'value verification failed.'
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

    def verify_undefined(self) -> [Union, None]:
        keypaths_undefined = []

        for keypath in get_deep_keypaths(self.data):
            if keypath not in self.keypaths_verified:
                keypath_origin = keypath

                keypath: str = re.sub(r'\[\d+?]$', '', keypath)
                keypath: str = keypath.replace('.', '.branch.')
                keypath: str = re.sub(r'\[\d+?]', '.items', keypath)

                struct: dict = self.blueprint

                for k in keypath.split('.'):
                    try:
                        struct: dict = struct[k]
                    except KeyError:
                        keypaths_undefined.append(keypath_origin)
                        break
                    else:
                        if k not in ('branch', 'items') and 'set' in struct:
                            break

        if keypaths_undefined:
            if len(keypaths_undefined) == 1:
                keypaths_undefined = keypaths_undefined[0]
            return {
                'title': 'UndefinedError',
                'keypath': keypaths_undefined,
                'msg': 'keypath is not defined on blueprint.'
            }


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


def getopt(*options, boole: bool = False) -> Union[str, bool, None]:
    args:  list = sys.argv[1:]
    index: int  = len(args) - 1

    while index > -1:
        value: str = args[index]

        if value in options:
            if boole:
                return True
            if index + 1 < len(args) and args[index + 1][0] != '-':
                return args[index + 1]
            raise ge.GetOptionError(f'option "{value}" need a parameter.')

        for opt in options:
            if value.startswith(opt + '='):
                if boole:
                    x: str = value.split("=", 1)[0]
                    raise ge.GetOptionError(f'option "{x}" takes no parameter.')
                return value.split('=', 1)[1]

        index -= 1

    if boole:
        return False


def gimport(path: str, attr: str = None, *, define=None) -> Any:
    try:
        __import__(path)
        module_ = sys.modules[path]
        return getattr(module_, attr) if attr else module_
    except (ValueError, ModuleNotFoundError, AttributeError):
        if define is not None:
            return define
        raise


def isempty(value: Any) -> bool:
    if value in (None, '', ...):
        return True
    try:
        if len(value) == 0:
            return True
    except TypeError:
        return False


def get_deep_keypaths(data: ..., *, __keypath__=None) -> Generator:
    if isinstance(data, dict):
        for key, value in data.items():
            keypath = f'{__keypath__}.{key}' if __keypath__ else key
            yield from get_deep_keypaths(value, __keypath__=keypath)
    elif isinstance(data, (tuple, list, set, frozenset)):
        for i, value in enumerate(data):
            keypath = f'{__keypath__}[{i}]' if __keypath__ else f'[{i}]'
            yield from get_deep_keypaths(value, __keypath__=keypath)
    elif __keypath__:
        yield __keypath__


verify_method_supported = [
    x[7:] for x in dir(DataStruct) if x[:7] == 'verify_'
] + ['default']
