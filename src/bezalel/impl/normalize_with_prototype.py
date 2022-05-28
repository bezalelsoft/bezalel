

def normalize_with_prototype(prototype, object_to_norm, path="", freestyle_attrs_name="freestyle_attrs"):
    if isinstance(prototype, dict):
        normalized_object = {}
        if object_to_norm is None:
            object_to_norm = {}
        if not isinstance(object_to_norm, dict):
            raise Exception(f"{path}: object_to_norm is not dict")
        for k, v in prototype.items():
            if k != "":
                normalized_object[k] = normalize_with_prototype(prototype[k], object_to_norm.get(k), path=f"{path}.{k}", freestyle_attrs_name=freestyle_attrs_name)
            else:
                normalized_object[freestyle_attrs_name] = [
                    {"key": key, "value": value} for key, value in object_to_norm.items() if key not in prototype.keys() or key == ""
                ]
        return normalized_object
    elif isinstance(prototype, list):
        if object_to_norm is None:
            object_to_norm = []
        if not isinstance(object_to_norm, list):
            raise Exception(f"{path}: object_to_norm is not list")
        return [normalize_with_prototype(prototype[0], e, path=f"{path}[{idx}]", freestyle_attrs_name=freestyle_attrs_name) for idx, e in enumerate(object_to_norm)]
    elif isinstance(prototype, str):
        if object_to_norm is None:
            return None
        if type(prototype) != type(object_to_norm):
            raise Exception(f"{path}: type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
        return object_to_norm
    elif isinstance(prototype, bool):
        if object_to_norm is None:
            return None
        if type(prototype) != type(object_to_norm):
            raise Exception(f"{path}: type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
        return object_to_norm
    elif isinstance(prototype, int):
        if object_to_norm is None:
            return None
        if not isinstance(prototype, (int, float)):
            raise Exception(f"{path}: expecting int or float, got {type(object_to_norm)} (of value {object_to_norm})")
        if type(object_to_norm) != int:
            object_to_norm = int(object_to_norm)
        return object_to_norm
    elif isinstance(prototype, float):
        if object_to_norm is None:
            return None
        if not isinstance(prototype, (int, float)):
            raise Exception(f"{path}: expecting int or float, got {type(object_to_norm)} (of value {object_to_norm})")
        if type(object_to_norm) != float:
            object_to_norm = float(object_to_norm)
        return object_to_norm
    else:
        raise Exception(f"{path}: prototype data type not supported: {type(prototype)}")

