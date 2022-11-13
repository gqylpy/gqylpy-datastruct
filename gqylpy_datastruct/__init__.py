"""
Create a blueprint to draw the data structure of your program, and then use this
blueprint to verify that the incoming data is correct.

    >>> from gqylpy_datastruct import DataStruct
    >>> datastruct = DataStruct({'name': {type: str}})
    >>> err = datastruct.verify({'name': 'Alpha'})

    @version: 1.0.3
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-datastruct

────────────────────────────────────────────────────────────────────────────────
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


class DataStruct:

    def __init__(self, blueprint: dict):
        """
        @param blueprint:
            Receive a data blueprint.

            See the documentation at
                https://github.com/gqylpy/gqylpy-datastruct

            We provide an example in
                https://github.com/gqylpy/gqylpy-datastruct/blob/master/test.py
        """
        __verify_and_upgrade__(blueprint)
        self.blueprint = blueprint

    def verify(
            self,
            data:   dict,
            *,
            eraise: bool = None
    ) -> 'Union[dict, None]':
        """
        @param data:   Data to be verified.
        @param eraise: Default False, if set to True and verification fails then
                       raise exception.
        @return:       An error message, if the verification fails and parameter
                       `eraise` is false.
        """
        err: Union[dict, None] = __verify__(data, self.blueprint)

        if err and eraise:
            raise type(err.pop('title'), (Exception,), {})(err)

        return err


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    """  QYYYQLLYYYYYYYQLYYQYYQQQYQQYQQQQQQQQQQQQQQQQQQQQQQYYYQQQQQQYL
        YYYYQYLLQYLLYYQYYYYYYYQQYQYQYQQQQQQQQQQQQQQQQQQQQQQQYYYQQQQQQ
        QYYYYLPQYLPLYYYLLYYYYYYYYQQQYQQQQQQQQQQQQQQQQQQQQQQQYYYYQQQQQP
        QYYQLPLQYLLYYQPLLLYYYYYYQYYQYQQQQQQQQQQQQQQYQQQQQQQQYYQYQQQQQQP
       QYYQYLLYYYLLYQYLLYYYYYYYYQYYQYQYYYQQQQQQQQQQYQQQQQQYQQYQYYQQQQQYP
      LQYQYYYYQYYYYYQYYYYYYYYYYYYYYYQQYYYYYYYYYQQQQYQQQQQQYQQYQYYQQQQQQ P
      QYQQYYYYQYYYQQQYYYYYYYYQYQYYYYQQYYYQYQYYQQQQYQQQQQQQYQQYQYYQQQQQQ P
      QYQQYYYYQYYYQQQYYYYYYYYQYQYYYYYQYYYYQYYYQQQQYQQQQQQQYQQYQQYQQQQYYP
      QYQYYYYYQYYYQQQ PYLLLYP PLYYYYYYQYYYYYYQQQQYYQQQQQQYQQYQQQYQQQQYQ
      PQQYYYYYQYYQQYQQQQQQQQQQYP        PPLYQYQYQYQLQQQQQYQQYQQQYYQQQYY
       QQYYYYYQQYQLYQQPQQQQQL QYL           PPYYLYYLQYQQYYQYQQQQYYQPQYL
       YQYYYYQQQYQ  LYLQQQQQQYQQ           YQQQQQGQQQQQQYQYYQQQQYQPQYQ P
      L QYYYYQQLYQ   Y YPYQQQQQ           LQQQQQL YQQQQYQQYQYQQYYQQYQP P
        YYQYYQQ  Q    LQQQQQQY            YQYQQQQQQYYQYLQYQQYQQYYQYQL P
     Y  LYQLQQPL Y     P  P                QLLQQQQQ Q  PQQQQYQQYYQQL P
    P   PYQYQQQQPQ                         PQQQQQQY    QQYQYYQQYYQPP
    L    QQQYQ YYYY              PQ           L  P    LPQYQYYQQLQ P
    Y   PPQQYYL LYQL                                 PQLQYQQYQYQ  L
    Y     QQYQPP PYQY        PQ                      Q  QQYQYQYL  L
    Y     QQYYQ L  QYQP         PLLLLLYL           LQQ LQYYQQQP P L
     L   PPLQYYQ Y  LQQQ                         LQYQ  QYYYQQ     P
      L    Q  QYQ  Y  QQPYL                   PQYYYYPPQYYQQQP    L
       L    L  PQQL   LYQ  PQP             QL PYYYPLQLYQ  QY P   Y
         P   P    PQQP  QY  QLLQQP   LYYLQ   PQYPQQQP P  QY P   L
                       PYQYYY           PQ  PQ      L   Q P    L
              PQYLYYYPQ PLPL             L QY YQYYQYLYQQQ    P
            PYLLLLLYYYQ P  L    P         PYL  PQYYLLLLLLLQ
           LYPLLLLLLYYYY   Y  YQY     LLLPPY   LYYYLLLLLLLLY
           YLLLYLLLLLLYYQ  Q              PQ  YYYLLLLLLLLLLYP
          YLLLLLLLLLLLLLLYQQ              PYYQYYLLLLLLLLYYYLQ
          QLLLLLLLLLLLLLLLLLYYQYP        YQYYLLLLLLLLLLLLLLLQ
          YLLLLLLLLLLLLLLLLLLLYYYLLYYYLLLLLLLLLLLLLLLLLLLLLLYP
         PLLLLLLLLLLLLLLLLLLLLLLLYLLLLLLLLLLLLLLLLLLLLLLLYLYLL
         LLLLLLLLLLYYLLLLLLYLLLLLLLLLLLLLLLL GQYLPY LLLYLYLLLY
         QLLLLYYLYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYYYLLQ
         QLLLLLYYQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQLYYLLLQ
        LYLLYLLLQYYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLQYYYYYLYQ
        YLLLYYLLYQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLYYYYQLLLLY
        QLLLYYYYYQLLLLLLLLLLLLLLYLLLLLLLLLLLLLLLLLLLLYYYLQLLPLLQ
        YLYLLQYYYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYLLLLLYYQYYLLLLLQ
       LYLLLLLYYYQLLYLLLLLLLLLLLLYLYLLYYLLLLYLLLLLLLYYYQQLLLLLLLY
       YLLLLLLYYYQLLYLLLLLLLYLYLLLLLLLLLLLLLLLLLLLLYYYYQQLYLLLLLQ
       QLLLYLLLQYQLQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYYQYYLLLLLLLY
       QLLLLLLLLQQYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYQYYLLLLLLLQ
       QLLLLLLLLLQQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYYYLLLLLLLLLYL
       QLLLLYLYYLYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYYLLLLLLLLLQ
       YLLLLLLLYYLQLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLLLLYQYYLLLLLLLLLQ
       QLLLLLYLYYYYLLLLLPLLLLLLLYLYLLLLLLLLLLLLLLLLLLLQYYLLLLLLLLYP
       YYLYYLLYYYQLLLLLLLLYLLLLLLLLLLLLLLLLLLLLLLYLYLLYQYYLLLLLLYL
        QLLLLLLYQYLLLLLLLLLLLLLLLLLLLLLYYLYLLLLLLLLLLLYQQQQQQQLYL  """
    import sys

    __import__(f'{__name__}.{__name__[0]} {__name__[7:]}')
    gpack = sys.modules[__name__]
    gcode = globals()[f'{__name__[0]} {__name__[7:]}']

    for gname in globals():
        if gname[0] != '_' and hasattr(gcode, gname):
            gfunc = getattr(gcode, gname)
            gfunc.__module__ = __package__
            setattr(gpack, gname, gfunc)


from typing import Union
