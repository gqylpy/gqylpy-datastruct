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
__version__ = 1, 0, 'alpha10'
__author__ = '竹永康 <gqylpy@outlook.com>'
__source__ = 'https://github.com/gqylpy/gqylpy-datastruct'


class DataStruct:

    def __init__(self, blueprint: dict):
        """
        Define a data blueprint, see the example in __main__ below.

        Supported methods and order of execution:
            default, env, option, type, coerce, enum, set, verify, callback

        Value priority:
            option > env > value > default
        """
        self.blueprint: dict = copy.deepcopy(blueprint)

    def verify(self, data: dict, *, eraise: bool = False) -> 'Union[dict, None]':
        """
        Verify @param(data) matches @param(self), if the verification process
        detects an error, it immediately terminates and return this error message.

        @param data:       Data to be verified.
        @param eraise:     If true, throws an exception instead of return an error message.
        @return:           Error message or None.
        """
        err: dict = verify(data, self)

        if err and eraise:
            raise e[err.pop('title')](err)

        return err

from gqylpy_exception import (
    BlueprintStructureError,
    BlueprintVerifyMethodError,
    BlueprintTypeError,
    BlueprintOptionError,
    BlueprintOptionBoolError,
    BlueprintENVError,
    BlueprintCoerceError,
    BlueprintEnumError,
    BlueprintSetError,
    BlueprintVerifyError,
    BlueprintCallbackError,

    DataNotFoundError,
    DataTypeError,
    DataCoerceError,
    DataEnumError,
    DataSetError,
    DataVerifyError
)


class ______歌______琪______怡______玲______萍______云______:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gpack = sys.modules[__name__]
    gcode = globals()[f'g {__name__[7:]}']

    for gname in globals():
        if gname[0] != '_' and hasattr(gcode, gname):
            gfunc = getattr(gcode, gname)
            gfunc.__module__ = __package__
            setattr(gpack, gname, gfunc)


from typing import Union
