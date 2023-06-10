[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-datastruct.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-datastruct/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_datastruct)](https://pypi.org/project/gqylpy_datastruct)
[![License](https://img.shields.io/pypi/l/gqylpy_datastruct)](https://github.com/gqylpy/gqylpy-datastruct/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_datastruct)](https://pepy.tech/project/gqylpy_datastruct)

# gqylpy-datastruct

> 创建一张蓝图来规划好程序需要的数据结构，并在之后使用该蓝图去校验到来的数据是否如期。

_这是一个雏形。_

<kbd>pip3 install gqylpy_datastruct</kbd>

```python
from gqylpy_datastruct import DataStruct

datastruct = DataStruct({'name': {type: str}})
err = datastruct.verify({'name': 'Alpha'})
```

`gqylpy_datastruct` 对外提供了一个类 `DataStruct`，在获得 `DataStruct` 实例时传入蓝图，并在之后调用实例的 `verify`
方法时传入数据，若数据与蓝图不符，将返回（或抛出）错误信息。我们提供了一个
[完整的示例](https://github.com/gqylpy/gqylpy-datastruct/blob/master/test.py)
，运用了该框架的大部分功能，阅读此文档必看此示例。

在获得 `DataStruct` 实例时传入蓝图，同时会校验蓝图，根据蓝图中定义 `key` 的顺序，从前往后，由浅入深进行校验，蓝图
`{a: {b: {c: ...}}, d: {e: ...}}` 的校验顺序是 `a` `a.b` `a.b.c` `d` `d.e`。校验后将蓝图存入属性 
`blueprint`，否则将在检查到第一个错误后立即抛出异常。

在之后调用实例的 `verify` 方法时传入数据，此时开始校验数据。校验过程是递归的，以蓝图作为递归主体，根据蓝图中定义 `key`
的顺序，从前往后，由浅入深从数据中取值。若 `key` 在数据中不存在，并且没有定义任何取值方法和默认值或定义的取值方法未取到值，并且未声明 `key`
是可选的，将立即返回 `DataNotFoundError`。取值后开始调用校验方法，按如下列出校验方法的前后顺序执行，全部校验通过最后执行回调
`callback`，否则将在检查到第一个错误后立即终止校验并返回错误信息。

> __取值方法__
> 
> <kbd>`option`</kbd>  
> 从命令行选项中取值并更新到数据中。指定一个选项用 `"--password"`，指定多个选项用
`("-p", "--password", ...)`。若未取到值则不做处理。优先级高于取值方法 `env` 和默认值 `default`。
> 
> <kbd>`option_bool`</kbd>  
> 检索命令行中有无指定的选项而更新数据中的值为 `True` 或 `False`，它是 `option` 的扩展，优先级同 `option`。`option`
和 `option_bool` 不可同时定义，否则将抛出 `BlueprintStructureError`。
> 
> <kbd>`env`</kbd>  
> 从环境变量中取值并更新到数据中。若未取到值则不做处理，优先级低于其它取值方法，高于默认值。

> __默认值__
> 
> <kbd>`default`</kbd>  
> 若 `key` 在数据中不存在，将创建 `key` 并用之为 `value`。

> __可选参数__
> 
> <kbd>`params`</kbd>  
> 使用元祖或列表指定一个或多个可选参数，可选的参数如下。  
> `optional`: 声明 `key` 是可选的，若 `key` 在数据中不存在，则跳过校验。  
> `delete_none`: 若值是 `None`，则跳过校验，并将其键值对从数据中删除。  
> `delete_empty`: 若值是空的，则跳过校验，并将其键值对从数据中删除。这里的空包括：`None`，`...`，`""`，以及任何长度等于0的容器。  
> `ignore_none`: 若值是 `None`，则跳过校验。优先级低于 `delete_none` 和 `delete_empty`。  
> `ignore_empty`: 若值是空的，则跳过校验。优先级低于 `delete_none` 和 `delete_empty`。  

> __校验方法__
> 
> <kbd>`delete_if_in`</kbd>  
> 使用元祖或列表指定一个或多个不希望得到的值，若传入的值位于其中，则跳过校验，并将其键值对从数据中删除。
> 
> <kbd>`ignore_if_in`</kbd>  
> 使用元祖或列表指定一个或多个不需要校验的值，若传入的值位于其中，则跳过校验。优先级低于 `delete_if_in`。
>
> <kbd>`type`</kbd>  
> 指定一个类，若值不是这个类的实例并且也不是这个类的子类的实例，将返回 `DataTypeError`。其内部调用 `isinstance` 
方法，可使用元组或列表指定多个类。可指定的类有 `[int, float, bytes, str, tuple, list, set, frozenset, dict, bool, NoneType, 
> datetime.date, datetime.time, datetime.datetime, decimal.Decimal]`。校验方法 `type`
的定义是针对内置的基础的大众所熟知的类型进行校验，若要校验其它类型，可编写校验函数并传给校验方法 `verify`。
> 
> <kbd>`coerce`</kbd>  
> 转换值的类型，可转换为 `[int, float, bytes, str, tuple, list, set, dict, bool]`。若类型无法被转换，将返回 
> `DataCoerceError`。若要转换为其它类型，可编写回调函数并传给回调 `callback`。
> 
> <kbd>`enum`</kbd>  
> 枚举，列出一个或多个值，只能在给定的范围内选择一个值，否则将返回 `DataEnumError`。`enum` 的灵感来源于 MySQL 中的枚举类型。
> 
> <kbd>`set`</kbd>  
> 集合，列出至少两个值，只能在给定的范围内选择一个或多个值，否则将返回 
`DataSetError`。选择值时必须使用列表或元组，若只选择一个值，可直接传入，它会在校验通过后被套上列表。`set` 的灵感来源于 MySQL 中的集合类型。
> 
> <kbd>`verify`</kbd>  
> 使用正则或函数校验数据。可以是一个正则表达式字符串、`re.Pattern` 的实例、可调用对象、可调用对象的路径字符串。正则校验调用 
> `search` 方法，校验函数需要一个参数用于接收数据。若校验失败将返回 
> `DataVerifyError`。可使用列表或元组定义多个校验，使用列表定义的多个校验将以 `or` 的关系执行，元组则 
> `and`。校验方法 `verify` 将在下个版本拆分为 `regex` 和 `validator`，分别对应正则校验和函数校验。

> __回调__
> 
> <kbd>`callback`</kbd>  
> 指定一个回调函数，将在校验通过后执行，回调函数需要一个参数用于接收数据，并在执行完毕后将其返回值更新到数据中。

> __关键字__
> 
> <kbd>`branch`</kbd>  
> 蓝图关键字，当数据内层是一个字典时，用 `branch` 连接。
> 
> <kbd>`items`</kbd>  
> 蓝图关键字，当数据内层是一个列表时，用 `items` 连接。

我们提供了一个 [完整的示例](https://github.com/gqylpy/gqylpy-datastruct/blob/master/test.py)
，运用了该框架的大部分功能，学习此框架必看此示例。
