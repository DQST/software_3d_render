from typing import Sequence, Any


def group_by(elements: Sequence[Any], by: int):
    res = ()
    for e in elements:
        res += (e,)
        if len(res) == by:
            yield res
            res = ()
