"""
Create a blueprint to plan the necessary data structure for the program, and
then use that blueprint to verify if the incoming data is as expected.

    >>> from gqylpy_datastruct import DataStruct
    >>> datastruct = DataStruct({'name': {type: str}})
    >>> err = datastruct.verify({'name': 'Alpha'})

    @version: 3.0
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-datastruct

────────────────────────────────────────────────────────────────────────────────
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
from typing import final, Optional, Union


@final
class DataStruct:
    """
    Create a data structure blueprint for your program, and use it to validate
    incoming data for correctness.

    See the documentation at
        https://github.com/gqylpy/gqylpy-datastruct

    We provide an example in
        https://github.com/gqylpy/gqylpy-datastruct/blob/master/test.py
    """

    def __init__(
            self,
            blueprint: dict,
            *,
            eraise:                Optional[bool] = None,
            etitle:                Optional[str]  = None,
            ignore_undefined_data: Optional[bool] = None
    ):
        """
        @param blueprint
            Receive a data blueprint.

        @param eraise
            By default, error information is returned as a return value, but if
            you want to raise an exception based on this error information, can
            set this parameter to True.

        @param etitle
            The prefix of error information title, default is "Data".

        @param ignore_undefined_data
            For data not defined in the blueprint, an error information titled
            `DataUndefinedError` is returned. If you want to ignore undefined
            data, can set this parameter to True.

        All optional parameters have lower priority than the parameters in the
        `verify` method.
        """
        self.blueprint = blueprint

    def verify(
            self,
            data: dict,
            *,
            eraise:                Optional[bool] = None,
            etitle:                Optional[str]  = None,
            ignore_undefined_data: Optional[bool] = None
    ) -> Union[dict, None]:
        """
        @param data
            The data to be verified.

        @param eraise
            By default, error information is returned as a return value, but if
            you want to raise an exception based on this error information, can
            set this parameter to True.

        @param etitle
            The prefix of error information title, default is "Data".

        @param ignore_undefined_data
            For data not defined in the blueprint, an error information titled
            `DataUndefinedError` is returned. If you want to ignore undefined
            data, can set this parameter to True.

        @return: The error information if verification fails.
        """


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    gpack = globals()
    gpath = f'{__name__}.{__name__[0]} {__name__[7:]}'
    gcode = __import__(gpath, fromlist=...)

    for gname in gpack:
        try:
            assert gname[0] != '_'
            gfunc = getattr(gcode, gname)
            try:
                gcode.os.startfile
            except AttributeError:
                assert gcode.os.__file__[:-6] == __file__[:-len(__name__) - 27]
            finally:
                assert gfunc.__module__ == gpath
        except (AssertionError, AttributeError):
            continue
        gfunc.__module__ = __package__
        gfunc.__doc__ = gpack[gname].__doc__
        gpack[gname] = gfunc
