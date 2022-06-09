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
__version__ = 1, 0, 'alpha3'


class DataBlueprint:

    def __init__(self, blueprint: dict):
        """
        Define a data blueprint, see the example in __main__ below.

        Supported methods and order of execution:
            default, env, option, type, coerce, enum, set, verify, callback

        Value priority:
            option > env > value > default
        """
        self.blueprint: dict = verify_blueprint_and_upgrade(blueprint)

    def verify(self, data: dict, *, else_raise: bool = False) -> 'Union[dict, None]':
        """
        Verify @param(data) matches @param(self), if the verification process
        detects an error, it immediately terminates and return this error message.

        @param data:       Data to be verified.
        @param else_raise: If true, throws an exception instead of return an error message.
        @return:           Error message or None.
        """
        err: dict = DataValidator(data, self)
        if err:
            if else_raise:
                raise e[err.pop('title')](err)
            return err


import gqylpy_exception as e

BlueprintTypeError         = e.BlueprintTypeError
BlueprintLimbError         = e.BlueprintLimbError
BlueprintStructureError    = e.BlueprintStructureError
BlueprintVerifyMethodError = e.BlueprintVerifyMethodError
BlueprintBranchDefineError = e.BlueprintBranchDefineError
BlueprintItemsDefineError  = e.BlueprintItemsDefineError
BlueprintOptionError       = e.BlueprintOptionError
BlueprintENVError          = e.BlueprintENVError
BlueprintCoerceError       = e.BlueprintCoerceError
BlueprintEnumError         = e.BlueprintEnumError
BlueprintSetError          = e.BlueprintSetError
BlueprintVerifyError       = e.BlueprintVerifyError
BlueprintCallbackError     = e.BlueprintCallbackError

DataTypeError     = e.DataTypeError
DataNotFoundError = e.DataNotFoundError
DataCoerceError   = e.DataCoerceError
DataEnumError     = e.DataEnumError
DataSetError      = e.DataSetError
DataVerifyError   = e.DataVerifyError


class _______G________Q________Y_______L_______P_______Y_______:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gpack = sys.modules[__name__]
    gcode = globals()[f'g {__name__[7:]}']

    for gname in globals():
        if gname[0] != '_' and hasattr(gcode, gname):
            setattr(gpack, gname, getattr(gcode, gname))


from typing import Union
