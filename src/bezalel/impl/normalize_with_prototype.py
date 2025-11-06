import datetime


class NormalizeException(Exception):
    def __init__(self, path, message):
        super().__init__(f"{path}: {message}")
        self._path = path
        self._message = message


def normalize_with_prototype(prototype, object_to_norm, freestyle_attrs_name="freestyle_attrs", pass_through_paths=[],
                             strict_types=True, type_converter=None):
    """
    Normalize python dict, so that it has all the fields and only the fields specified in a prototype dict.

    :param prototype: A prototype dict, for example from Swagger doc.
    :param object_to_norm: A dict that comes from API.
    :param freestyle_attrs_name: it is a name for attribute, when prototype contains a dict like this: "field": {"": ""}
    :param pass_through_paths: list of paths which will be passed through without normalization (for example dicts with
        unpredicted structure, that will be handled after normalization)
    :param strict_types: if True, then fail on types mismatch between prototype and object_to_norm.
        If False, function will attempt to parse string, i.e. "123.45" to 123.45 float.
        It will fail on parsing errors anyway.
    :param type_converter: a function with signature:
        type_converter(prototype_object: any, object_to_norm: any, path_info: str) -> any
        called only when strict_types=False and type(prototype_object) != type(object_to_norm)
    :return:
    """
    if not type_converter:
        type_converter = lambda prototype_object, object_to_norm, path_info: object_to_norm

    def normalize_with_prototype_rec(prototype, object_to_norm, path_info, prototype_path):
        try:
            if prototype_path in pass_through_paths:
                return object_to_norm
            if isinstance(prototype, dict):
                if object_to_norm is None:
                    object_to_norm = {}
                elif not isinstance(object_to_norm, dict) and not strict_types:
                    object_to_norm = type_converter(prototype, object_to_norm, path_info)
                if not isinstance(object_to_norm, dict):
                    raise NormalizeException(path_info, f"object_to_norm is not dict (of value {object_to_norm})")
                normalized_object = {}
                for k, v in prototype.items():
                    if k != "":
                        normalized_object[k] = normalize_with_prototype_rec(prototype[k], object_to_norm.get(k), path_info=f"{path_info}.{k}", prototype_path=f"{prototype_path}.{k}" if prototype_path != "" else k)
                    else:
                        normalized_object[freestyle_attrs_name] = [
                            {"key": key, "value": value} for key, value in object_to_norm.items() if key not in prototype.keys() or key == ""
                        ]
                return normalized_object
            elif isinstance(prototype, list):
                if object_to_norm is None:
                    object_to_norm = []
                elif not isinstance(object_to_norm, list) and not strict_types:
                    object_to_norm = type_converter(prototype, object_to_norm, path_info)
                if not isinstance(object_to_norm, list):
                    raise NormalizeException(path_info, f"object_to_norm is not list (of value {object_to_norm})")
                return [normalize_with_prototype_rec(prototype[0], e, path_info=f"{path_info}[{idx}]", prototype_path=prototype_path) for idx, e in enumerate(object_to_norm)]
            elif isinstance(prototype, str):
                if object_to_norm is None:
                    return None
                if type(prototype) != type(object_to_norm):
                    if strict_types:
                        raise NormalizeException(path_info, f"type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
                    else:
                        return str(type_converter(prototype, object_to_norm, path_info))
                return object_to_norm
            elif isinstance(prototype, bool):
                if object_to_norm is None:
                    return None
                if type(prototype) != type(object_to_norm):
                    if strict_types:
                        raise NormalizeException(path_info, f"type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
                    else:
                        object_to_norm = type_converter(prototype, object_to_norm, path_info)
                        if not isinstance(object_to_norm, bool):
                            if isinstance(object_to_norm, str):
                                if object_to_norm.lower().strip() in {'1', 'true', 'yes'}:
                                    object_to_norm = True
                                elif object_to_norm.lower().strip() in {'0', 'false', 'no'}:
                                    object_to_norm = False
                                else:
                                    object_to_norm = None
                            else:
                                object_to_norm = bool(object_to_norm)
                return object_to_norm
            elif isinstance(prototype, int):
                if object_to_norm is None:
                    return None
                if not isinstance(object_to_norm, int):
                    if strict_types:
                        raise NormalizeException(path_info, f"type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
                    else:
                        if isinstance(object_to_norm, str) and object_to_norm.strip() == "":
                            return None
                        try:
                            object_to_norm = int(type_converter(prototype, object_to_norm, path_info))
                        except Exception as e:
                            raise NormalizeException(path_info, f"can't parse int '{object_to_norm}': {e}")
                return object_to_norm
            elif isinstance(prototype, float):
                if object_to_norm is None:
                    return None
                if not isinstance(object_to_norm, (int, float)):
                    if strict_types:
                        raise NormalizeException(path_info, f"type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
                    else:
                        if isinstance(object_to_norm, str) and object_to_norm.strip() == "":
                            return None
                        try:
                            object_to_norm = float(type_converter(prototype, object_to_norm, path_info))
                        except Exception as e:
                            raise NormalizeException(path_info, f"can't parse float '{object_to_norm}': {e}")
                if not isinstance(object_to_norm, float):
                    try:
                        object_to_norm = float(object_to_norm)
                    except Exception as e:
                        raise NormalizeException(path_info, f"can't parse float '{object_to_norm}': {e}")
                return object_to_norm
            elif isinstance(prototype, datetime.datetime):
                # datetime.datetime() is an instance of both datetime.datetime and datetime.date.
                # datetime.date() is NOT an instance of datetime.datetime
                # that's why `isinstance(prototype, datetime.datetime)` check comes before `isinstance(prototype, datetime.date)`.
                if object_to_norm is None:
                    return None
                if not isinstance(object_to_norm, datetime.datetime):
                    if strict_types:
                        raise NormalizeException(path_info, f"type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
                    else:
                        if isinstance(object_to_norm, str) and object_to_norm.strip() == "":
                            return None
                        try:
                            object_to_norm = type_converter(prototype, object_to_norm, path_info)
                            if not isinstance(object_to_norm, datetime.datetime):
                                object_to_norm = datetime.datetime.fromisoformat(object_to_norm)
                        except Exception as e:
                            raise NormalizeException(path_info, f"can't parse datetime fromisoformat '{object_to_norm}': {e}")
                return object_to_norm
            elif isinstance(prototype, datetime.date):
                if object_to_norm is None:
                    return None
                if not isinstance(object_to_norm, datetime.date):
                    if strict_types:
                        raise NormalizeException(path_info, f"type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
                    else:
                        if isinstance(object_to_norm, str) and object_to_norm.strip() == "":
                            return None
                        try:
                            object_to_norm = type_converter(prototype, object_to_norm, path_info)
                            if not isinstance(object_to_norm, datetime.date):
                                object_to_norm = datetime.date.fromisoformat(object_to_norm)
                        except Exception as e:
                            raise NormalizeException(path_info, f"can't parse date fromisoformat '{object_to_norm}': {e}")
                if isinstance(object_to_norm, datetime.datetime):
                    object_to_norm = object_to_norm.date()
                return object_to_norm
            else:
                raise NormalizeException(path_info, f"prototype data type not supported: {type(prototype)}")
        except NormalizeException as e:
            raise
        except Exception as e:
            raise NormalizeException(path_info, str(e))
    return normalize_with_prototype_rec(prototype, object_to_norm, "", "")
