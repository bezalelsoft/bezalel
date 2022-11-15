from bezalel import normalize_with_prototype
from unittest import TestCase


def test_normalize_with_prototype_1():
    object_from_api = {
        "id": 123,
        "name:": "John",
        "country": "Poland",
        # city is not provided here (but present in prototype)
        "pets": [
            {"id": 101, "type": "dog", "name": "Barky"},
            {"id": 102, "type": "snail"},   # name is not provided here (but present in prototype)
        ],
        "unspecifiedField": 123     # this field is not present in prototype below
    }

    prototype_from_swagger = {
        "id": 0,
        "name:": "",
        "country": "",
        "city": "",
        "pets": [
            {"id": 0, "type": "", "name": ""},
        ]
    }

    result = normalize_with_prototype(prototype_from_swagger, object_from_api)

    expected_result = {
        "id": 123,
        "name:": "John",
        "country": "Poland",
        "city": None,   # city was added
        "pets": [
            {"id": 101, "type": "dog", "name": "Barky"},
            {"id": 102, "type": "snail", "name": None}, # name was added
        ]
    }

    TestCase().assertDictEqual(expected_result, result)

    TestCase().assertDictEqual(expected_result, normalize_with_prototype(prototype_from_swagger, result))
    print(result)


def test_normalize_with_prototype_pass_through():
    object_from_api = {
        "id": 123,
        "name:": "John",
        "country": "Poland",
        "customDict": {
            "some": 123,
            "complex": 345,
            "structure": 546
        },
        # city is not provided here (but present in prototype)
        "pets": [
            {"id": 101, "type": "dog", "name": "Barky"},
            {"id": 102, "type": "snail"},   # name is not provided here (but present in prototype)
        ],
        "unspecifiedField": 123     # this field is not present in prototype below
    }

    prototype_from_swagger = {
        "id": 0,
        "name:": "",
        "country": "",
        "customDict": {},
        "city": "",
        "pets": [
            {"id": 0, "type": "", "name": ""},
        ]
    }

    result = normalize_with_prototype(prototype_from_swagger, object_from_api, pass_through_paths=["customDict"])

    expected_result = {
        "id": 123,
        "name:": "John",
        "country": "Poland",
        "customDict": {
            "some": 123,
            "complex": 345,
            "structure": 546
        },
        "city": None,   # city was added
        "pets": [
            {"id": 101, "type": "dog", "name": "Barky"},
            {"id": 102, "type": "snail", "name": None}, # name was added
        ]
    }

    TestCase().assertDictEqual(expected_result, result)

    TestCase().assertDictEqual(expected_result, normalize_with_prototype(prototype_from_swagger, result, pass_through_paths=["customDict"]))
    print(result)


def test_normalize_with_prototype_pass_through_in_array():
    object_from_api = {
        "id": 123,
        "name:": "John",
        "country": "Poland",
        # city is not provided here (but present in prototype)
        "pets": [
            {"id": 101, "type": "dog", "name": "Barky", "customDict": {"some": 123,"complex": 345,"structure": 546}},
            {"id": 102, "type": "snail", "customDict": {"booo": 777}},   # name is not provided here (but present in prototype)
        ],
        "unspecifiedField": 123     # this field is not present in prototype below
    }

    prototype_from_swagger = {
        "id": 0,
        "name:": "",
        "country": "",
        "city": "",
        "pets": [
            {"id": 0, "type": "", "name": "", "customDict": {}},
        ]
    }

    result = normalize_with_prototype(prototype_from_swagger, object_from_api, pass_through_paths=["pets.customDict"])

    expected_result = {
        "id": 123,
        "name:": "John",
        "country": "Poland",
        "city": None,   # city was added
        "pets": [
            {"id": 101, "type": "dog", "name": "Barky", "customDict": {"some": 123,"complex": 345,"structure": 546}},
            {"id": 102, "type": "snail", "name": None, "customDict": {"booo": 777}}, # name was added
        ]
    }

    TestCase().assertDictEqual(expected_result, result)

    TestCase().assertDictEqual(expected_result, normalize_with_prototype(prototype_from_swagger, result, pass_through_paths=["pets.customDict"]))
    print(result)
