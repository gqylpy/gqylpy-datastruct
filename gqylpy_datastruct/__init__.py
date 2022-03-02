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

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
__version__ = 1, 0, 'dev1'


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

    for gname, ifunc in globals().items():
        if gname[0] != '_' and hasattr(gcode, gname):
            setattr(gpack, gname, getattr(gcode, gname))


from typing import Union
