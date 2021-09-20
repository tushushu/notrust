"""
Author: tushushu
Date: 2021-09-20 12:36:18
"""

from functools import reduce
from itertools import chain, product
from typing import Any, Callable, Dict, Iterable, List, Set, Tuple, Union


class _Calculation:
    def __init__(self, op: Callable, args: Tuple[Any, ...]) -> None:
        self.op = op
        self.args = args


class Iter:
    def __init__(self, obj: Iterable, execute_plan: List[_Calculation] = None) -> None:
        self.obj = obj
        if execute_plan is None:
            self.execute_plan = []
        else:
            self.execute_plan = execute_plan

    def _map(self, obj: Iterable, func: Callable) -> Iterable:
        return map(func, obj)

    def map(self, func: Callable) -> 'Iter':
        self.execute_plan.append(
            _Calculation(
                op=self._map,
                args=(func, ),
            )
        )
        return self

    def _flatten(self, obj: Iterable) -> Iterable:
        return chain(*obj)

    def flatten(self) -> 'Iter':
        self.execute_plan.append(
            _Calculation(
                op=self._flatten,
                args=(),
            )
        )
        return self

    def _zip(self, obj: Iterable, *args: Tuple[Any, ...]) -> Iterable:
        return zip(obj, *args)

    def zip(self, *args) -> 'Iter':
        self.execute_plan.append(
            _Calculation(
                op=self._zip,
                args=args,
            )
        )
        return self

    def _product(self, obj: Iterable, *args: Tuple[Any, ...]) -> Iterable:
        return product(obj, *args)

    def product(self, *args: Tuple[Any, ...]) -> 'Iter':
        self.execute_plan.append(
            _Calculation(
                op=self._product,
                args=args,
            )
        )
        return self

    def _filter(self, obj: Iterable, func: Callable) -> Iterable:
        return (x for x in obj if func(x))

    def filter(self, func: Callable) -> 'Iter':
        self.execute_plan.append(
            _Calculation(
                op=self._filter,
                args=(func,),
            )
        )
        return self

    def _groupby(self, obj: Iterable, key_func: Callable, val_func: Callable) -> Iterable:
        result: Dict[Any, List[Any]] = dict()
        for x in obj:
            if key_func(x) in result:
                result[key_func(x)].append(val_func(x))
            else:
                result[key_func(x)] = [val_func(x)]
        return result.items()

    def groupby(self, key_func: Callable, val_func: Callable) -> 'Iter':
        self.execute_plan.append(
            _Calculation(
                op=self._groupby,
                args=(key_func, val_func),
            )
        )
        return self

    def _execute(self) -> Any:
        obj = self.obj
        for calculation in self.execute_plan:
            obj = calculation.op(obj, *calculation.args)
        self.execute_plan = []
        return obj

    def _reduce(self, obj: Iterable, func: Callable, initial=None) -> Any:
        if initial is not None:
            return reduce(func, obj, initial=initial)
        return reduce(func, obj)

    def reduce(self, func: Callable, initial=None) -> Any:
        self.execute_plan.append(
            _Calculation(
                op=self._reduce,
                args=(func, initial),
            )
        )
        return self._execute()

    def sum(self) -> Union[int, float]:
        self.execute_plan.append(
            _Calculation(
                op=sum,
                args=(),
            )
        )
        return self._execute()

    def _count(self, obj) -> int:
        if hasattr(obj, '__len__'):
            return len(obj)
        return sum(1 for x in obj)

    def count(self) -> int:
        self.execute_plan.append(
            _Calculation(
                op=self._count,
                args=(),
            )
        )
        return self._execute()

    def to_data(self, dtype) -> Any:
        if dtype == "dict":
            op = dict
        elif dtype == "set":
            op = set  # type: ignore
        elif dtype == "list":
            op = list  # type: ignore
        else:
            raise ValueError
        self.execute_plan.append(
            _Calculation(
                op=op,
                args=(),
            )
        )
        return self._execute()

    def to_dict(self) -> Dict[Any, Any]:
        return self.to_data("dict")

    def to_list(self) -> List[Any]:
        return self.to_data("list")

    def to_set(self) -> Set[Any]:
        return self.to_data("set")
