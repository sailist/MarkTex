from typing import Union, Dict, Any, List
import bisect


class MetaComparable(type):
    priority = 0

    def __new__(tcls, *args: Any, **kwargs: Any):
        cls = type.__new__(tcls, *args, **kwargs)
        if getattr(cls, 'priority', None) is None:
            cls.priority = tcls.priority
        return cls

    def __lt__(self, other):
        return self.priority > other.priority


def regist_func(val: Union[Dict[str, MetaComparable], List[MetaComparable]]):
    def wrap(func):
        bisect.insort(val, func)
        # val.insert(0, func)
        return func

    return wrap
