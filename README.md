[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Version](https://img.shields.io/pypi/v/gqylpy_datastruct)](https://pypi.org/project/gqylpy_datastruct/)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_datastruct)](https://pypi.org/project/gqylpy_datastruct)
[![License](https://img.shields.io/pypi/l/gqylpy_datastruct)](https://github.com/gqylpy/gqylpy-datastruct/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_datastruct/month)](https://pepy.tech/project/gqylpy_datastruct)

gqylpy-datastruct

> 创建一张蓝图来规划好程序需要的数据结构，并在之后使用该蓝图去校验所有到来的数据是否如期。

<kbd>pip3 install gqylpy_datastruct</kbd>

```python
from gqylpy_datastruct import DataStruct

datastruct = DataStruct({'name': {type: str}})
err: dict | None = datastruct.verify({'name': 'Alpha'})
```

`gqylpy_datastruct` 对外提供了一个 `DataStruct` 类，在获得 `DataStruct` 实例时传入蓝图，
并在之后调用实例的 `verify` 方法时传入数据，若数据与蓝图不符，将返回（或抛出）错误信息。
我们提供了一个 [教学示例](https://github.com/gqylpy/gqylpy-datastruct/blob/master/test.py) ，
运用了该框架的大部分功能，初识的你一定要看一看。

在获得 `DataStruct` 实例时传入蓝图，同时会校验蓝图，根据蓝图中定义 `key` 的顺序，从前往后，由浅入深进行校验，
蓝图 `{a: {b: c: ...}, d: {e: ...}` 的校验顺序是 `a` `a.b` `a.b.c` `d` `d.e` 。
校验通过后将蓝图对象存入属性 `blueprint`，否则将在检查到第一个错误后抛出异常。

###### 蓝图关键字

___
用于校验数据

__关键字 `type`__  
定义数据的类型，可定义的类型有：
<font color=gray>int, float, str, bytes, list, tuple, set, dict, bool, NoneType, datetime.date, datetime.time, datetime.datetime</font> 。  
若传入的数据的类型与定义的类型不符，将返回 `DataTypeError` 。  

__关键字 `coerce`__  
转换数据的类型，可转换为 <font color=gray>int, float, str, bytes, list, tuple, set, dict, bool</font> 。  
若无法将数据转换为指定类型，将返回 `DataCoerceError` 。

__关键字 `enum`__  
枚举，列出几个值，若传入的数据不在其中，将返回 `DataEnumError` 。

__关键字 `set`__  

__关键字 `verify`__  

__关键字 `callback`__  
<br>

用于取值
___

__关键字 `default`__  

__关键字 `env`__  

__关键字 `option`__  

__关键字 `option_bool`__  

___

__关键字 `branch`__  

__关键字 `items`__  
