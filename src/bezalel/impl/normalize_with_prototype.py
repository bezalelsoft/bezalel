

def normalize_with_prototype(prototype, object_to_norm, freestyle_attrs_name="freestyle_attrs", pass_through_paths=[]):
    """
    Normalize python dict, so that it has all the fields and only the fields specified in a prototype dict.

    :param prototype: A prototype dict, for example from Swagger doc
    :param object_to_norm: A dict that comes from API
    :param freestyle_attrs_name: it is a name for attribute, when prototype contains a dict like this: "field": {"": ""}
    :param pass_through_paths: list of paths which will be passed through without normalization (for example dicts with
        unpredicted structure, that will be handled after normalization)
    :return:
    """
    def normalize_with_prototype_rec(prototype, object_to_norm, path_info, prototype_path):
        if prototype_path in pass_through_paths:
            return object_to_norm
        if isinstance(prototype, dict):
            normalized_object = {}
            if object_to_norm is None:
                object_to_norm = {}
            if not isinstance(object_to_norm, dict):
                raise Exception(f"{path_info}: object_to_norm is not dict")
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
            if not isinstance(object_to_norm, list):
                raise Exception(f"{path_info}: object_to_norm is not list")
            return [normalize_with_prototype_rec(prototype[0], e, path_info=f"{path_info}[{idx}]", prototype_path=prototype_path) for idx, e in enumerate(object_to_norm)]
        elif isinstance(prototype, str):
            if object_to_norm is None:
                return None
            if type(prototype) != type(object_to_norm):
                raise Exception(f"{path_info}: type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
            return object_to_norm
        elif isinstance(prototype, bool):
            if object_to_norm is None:
                return None
            if type(prototype) != type(object_to_norm):
                raise Exception(f"{path_info}: type(prototype) != type(object_to_norm): {type(prototype)} != {type(object_to_norm)} (of value {object_to_norm})")
            return object_to_norm
        elif isinstance(prototype, int):
            if object_to_norm is None:
                return None
            if not isinstance(prototype, (int, float)):
                raise Exception(f"{path_info}: expecting int or float, got {type(object_to_norm)} (of value {object_to_norm})")
            if type(object_to_norm) != int:
                object_to_norm = int(object_to_norm)
            return object_to_norm
        elif isinstance(prototype, float):
            if object_to_norm is None:
                return None
            if not isinstance(prototype, (int, float)):
                raise Exception(f"{path_info}: expecting int or float, got {type(object_to_norm)} (of value {object_to_norm})")
            if type(object_to_norm) != float:
                object_to_norm = float(object_to_norm)
            return object_to_norm
        else:
            raise Exception(f"{path_info}: prototype data type not supported: {type(prototype)}")
    return normalize_with_prototype_rec(prototype, object_to_norm, "", "")
