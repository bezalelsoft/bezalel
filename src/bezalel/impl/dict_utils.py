from typing import Optional


def dict_get(d: dict, path: str, default: any = None, path_split_char: str = ".") -> any:
    elems = path.split(path_split_char)
    q = d
    for e in elems:
        if not isinstance(q, dict):
            return default
        if e in q.keys():
            q = q.get(e)
        else:
            return default
    return q


def dict_set(d: dict, path: str, val: any, path_split_char: str = "."):
    elems = path.split(path_split_char)

    q = d
    for e in elems[:-1]:
        if e in q.keys():
            if isinstance(q.get(e), dict):
                q = q.get(e)
            else:
                q[e] = {}
                q = q.get(e)
        else:
            q[e] = {}
            q = q[e]
    k = elems[-1]
    q[k] = val

