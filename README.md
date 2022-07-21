[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Version](https://img.shields.io/pypi/v/gqylpy_datastruct)](https://pypi.org/project/gqylpy_datastruct/)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_datastruct)](https://pypi.org/project/gqylpy_datastruct)
[![License](https://img.shields.io/pypi/l/gqylpy_datastruct)](https://github.com/gqylpy/gqylpy-datastruct/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_datastruct/month)](https://pepy.tech/project/gqylpy_datastruct)

# gqylpy-datastruct

> 创建一张蓝图来规划好程序需要的数据结构，并在之后使用该蓝图去校验到来的数据是否如期。

<kbd>pip3 install gqylpy_datastruct</kbd>

```python
from gqylpy_datastruct import DataStruct

datastruct = DataStruct({'name': {type: str}})
err: dict | NoneType = datastruct.verify({'name': 'Alpha'})
```

`gqylpy_datastruct` 对外提供了一个类 `DataStruct`，在获得 `DataStruct` 实例时传入蓝图，并在之后调用实例的 `verify`
方法时传入数据，若数据与蓝图不符，将返回（或抛出）错误信息。我们提供了一个
[完整的示例](https://github.com/gqylpy/gqylpy-datastruct/blob/master/test.py) ，运用了该框架的大部分功能，初识的你一定要看一看。

在获得 `DataStruct` 实例时传入蓝图，同时会校验蓝图，根据蓝图中定义 `key` 的顺序，从前往后，由浅入深进行校验，蓝图
`{a: {b: {c: ...}}, d: {e: ...}}` 的校验顺序是 `a` `a.b` `a.b.c` `d` `d.e`。校验后将蓝图对象存入属性 
`blueprint`，否则将在检查到第一个错误后立即抛出异常。

在之后调用实例的 `verify` 方法时传入数据，此时开始校验数据。校验过程是递归的，以蓝图作为递归主体，根据蓝图中定义 `key`
的顺序，从前往后，由浅入深从数据中取值。若 `key` 在数据中不存在，并且没有定义任何取值方法和默认值或定义的取值方法未取到值，将立即返回
`DataNotFoundError`。取值后开始调用校验方法，校验方法的调用顺序是固定的，如下方列出校验方法的前后顺序。
___
___

> __<font color=#158fb5>取值方法</font>__
> 
> <kbd><kbd>`option`</kbd></kbd>  
> 从命令行选项中取值并更新到数据中。指定一个选项用 `"--password"`，指定多个选项用
`("-p", "--password", ...)`。若未取到值则不做处理。优先级高于取值方法 `env` 和默认值 `default`。
> 
> <kbd><kbd>`option_bool`</kbd></kbd>  
> 检索命令行中有无指定的选项而更新数据中的值为 `True` 或 `False`，它是 `option` 的扩展，优先级同 `option`。`option`
和 `option_bool` 不可同时定义，否则将抛出 `BlueprintStructureError`。
> 
> <kbd><kbd>`env`</kbd></kbd>  
> 从环境变量中取值并更新到数据中。若未取到值则不做处理，优先级低于其它取值方法，高于默认值。

> __<font color=green>默认值</font>__
> 
> <kbd><kbd>`default`</kbd></kbd>  
> 若 `key` 在数据中不存在，将创建 `key` 并使用默认值作为其 `value`。

> __<font color=brown>校验方法</font>__
> 
> <kbd><kbd>`type`</kbd></kbd>  
> 指定一个类，若数据不是这个类的实例并且也不是这个类的子类的实例，将返回 `DataTypeError`。其内部调用 `isinstance` 
方法，可使用元组或列表指定多个类。可指定的类有 <font color=gray>int, float, str, bytes, list, tuple, set, 
dict, bool, NoneType, datetime.date, datetime.time, datetime.datetime</font>。校验方法 `type`
的定义是针对内置的基础的大众所熟知的类型进行校验，若要校验其它类型，可编写校验函数并传给校验方法 `verify`。
> 
> <kbd><kbd>`coerce`</kbd></kbd>  
> 转换数据的类型，可转换为 <font color=gray>int, float, str, bytes, list, tuple, set, dict, 
bool</font>。若类型无法被转换，将返回 `DataCoerceError`。若要转换为其它类型，可编写回调函数并传给回调 `callback`。
> 
> <kbd><kbd>`enum`</kbd></kbd>  
> 枚举，列出一个或多个值，只能在给定的范围内选择一个值，否则将返回 `DataEnumError`。`enum` 的灵感来源于 MySQL 中的枚举类型。
> 
> <kbd><kbd>`set`</kbd></kbd>  
> 集合，列出至少两个值，只能在给定的范围内选择一个或多个值，否则将返回 
`DataSetError`。选择值时必须使用列表或元组，若只选择一个值，可直接传入，它会在校验通过后被套上列表。`set` 的灵感来源于 MySQL 中的集合类型。
> 
> <kbd><kbd>`verify`</kbd></kbd>  
> 使用正则或函数校验数据。可以是一个正则表达式字符串、`re.Pattern` 的实例、可调用对象、可调用对象的路径字符串。正则校验调用 `search` 
方法，可调用对象必须有一个参数用来接收数据。可使用列表或元组

> __<font color=#FFC66D>回调</font>__
> 
> <kbd><kbd>`callback`</kbd></kbd>  
> 回调函数

> __<font color=#CC7832>关键字</font>__
> 
> <kbd><kbd>`branch`</kbd></kbd>  
> 连接子字典
> 
> <kbd><kbd>`items`</kbd></kbd>  
> 连接子列表
