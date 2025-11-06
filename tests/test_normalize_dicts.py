from pprint import pprint
from bezalel import normalize_dicts
from unittest import TestCase
import json

class TestNormalizeDicts(TestCase):
    def test_simple_case_1(self):
        data = [
            {
                "id": 1, "name": "John Smith",
                "pets": [
                    {"id": 101, "type": "cat", "name": "Kitty", "toys": [{"name": "toy1"}, {"name": "toy2"}]},
                    {"id": 102, "type": "dog", "name": "Barky", "toys": [{"name": "toy3"}]}
                ]
            },
            {
                "id": 2, "name": "Sue Smith",
                "pets": [
                    {"id": 201, "type": "cat", "name": "Kitten", "toys": [{"name": "toy4"}, {"name": "toy5"}, {"name": "toy6"}]},
                    {"id": 202, "type": "dog", "name": "Fury", "toys": []}
                ]
            },
        ]

        expected_list = [
            {'id': 1, 'name': 'John Smith', 'pets.id': 101, 'pets.type': 'cat', 'pets.name': 'Kitty', 'pets.toys.name': 'toy1'},
            {'id': 1, 'name': 'John Smith', 'pets.id': 101, 'pets.type': 'cat', 'pets.name': 'Kitty', 'pets.toys.name': 'toy2'},
            {'id': 1, 'name': 'John Smith', 'pets.id': 102, 'pets.type': 'dog', 'pets.name': 'Barky', 'pets.toys.name': 'toy3'},
            {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy4'},
            {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy5'},
            {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy6'},
            {'id': 2, 'name': 'Sue Smith', 'pets.id': 202, 'pets.type': 'dog', 'pets.name': 'Fury'}]
        result = normalize_dicts(data, ["pets", "toys"])
        TestCase().assertListEqual(expected_list, result)


    def test_empty_input(self):
        data = []
        expected_list = []
        result = normalize_dicts(data, ["pets", "toys"])
        TestCase().assertListEqual(expected_list, result)


    def test_with_empty_list(self):
        data = [{
            "id": 1, "name": "Cole Volk", "fitness": [{"height": 130, "weight": 60}, {"height": 1300, "weight": 600}],
            "someList": []
        },
        {
            "id": 2, "name": "Faye Raker", "fitness": [{"height": 130, "weight": 60}, {"height": 888, "weight": 777}],
            "someList": [1]
        },
        {
            "id": 2, "name": "Faye Raker", "fitness": [{"height": 130, "weight": 60}],
            "someList": [1]
        },
        ]
        expected_list = [
            {'id': 1, 'name': 'Cole Volk', 'someList': [], 'fitness.height': 130, 'fitness.weight': 60},
            {'id': 1, 'name': 'Cole Volk', 'someList': [], 'fitness.height': 1300, 'fitness.weight': 600},
            {'id': 2, 'name': 'Faye Raker', 'someList': [1], 'fitness.height': 130, 'fitness.weight': 60},
            {'id': 2, 'name': 'Faye Raker', 'someList': [1], 'fitness.height': 888, 'fitness.weight': 777},
            {'id': 2, 'name': 'Faye Raker', 'someList': [1], 'fitness.height': 130, 'fitness.weight': 60}]
        result = normalize_dicts(data, ["fitness"])
        print(result)
        TestCase().assertListEqual(expected_list, result)


    def test_empty_lists_2(self):
        data = [{
            "id": 1, "name": "Cole Volk", "fitness": [{"height": 130, "weight": 60}],
            "someList": []
        },
        {
            "id": 2, "name": "Faye Raker", "fitness": [{"height": 130, "weight": 60}],
            "someList": []
        }, ]
        expected_list = [
            {'id': 1, 'name': 'Cole Volk', 'someList': [], 'fitness.height': 130, 'fitness.weight': 60},
            {'id': 2, 'name': 'Faye Raker', 'someList': [], 'fitness.height': 130, 'fitness.weight': 60}]
        result = normalize_dicts(data, ["fitness"])
        print(result)
        TestCase().assertListEqual(expected_list, result)


    def test_2_level(self):
        data = [{
            "id": 1, "name": "Cole Volk", "fitness": [
                {"fit1": 101, "fit2": [{"height": 1001, "weight": 1002}, {"height": 1011, "weight": 1012}, {"height": 1022, "weight": 1023}] },
                {"fit1": 102, "fit2": [{"height": 11, "weight": 22}]},
            ],
            "someList": []
        },
        {
            "id": 2, "name": "Faye Raker", "fitness": [
                {"fit1": 201,
                 "fit2": [{"height": 131, "weight": 601}, {"height": 132, "weight": 602}, {"height": 133, "weight": 603}]},
                {"fit1": 202, "fit2": [{"height": 11, "weight": 22}]},
            ],
            "someList": []
        },
        {},
        {"id": 3, "name": "AAA BBB", "fitness": []},
        {"id": 4, "name": "AAA BBB", "fitness": None},
        # {"id": 4, "name": "AAA BBB", "fitness": "not-a-list"} # TODO: it should throw an exception, so move it to another test
        ]

        expected_list = [{'id': 1, 'name': 'Cole Volk', 'someList': [], 'fitness.fit1': 101, 'fitness.fit2.height': 1001, 'fitness.fit2.weight': 1002},
                         {'id': 1, 'name': 'Cole Volk', 'someList': [], 'fitness.fit1': 101, 'fitness.fit2.height': 1011, 'fitness.fit2.weight': 1012},
                         {'id': 1, 'name': 'Cole Volk', 'someList': [], 'fitness.fit1': 101, 'fitness.fit2.height': 1022, 'fitness.fit2.weight': 1023},
                         {'id': 1, 'name': 'Cole Volk', 'someList': [], 'fitness.fit1': 102, 'fitness.fit2.height': 11, 'fitness.fit2.weight': 22},
                         {'id': 2, 'name': 'Faye Raker', 'someList': [], 'fitness.fit1': 201, 'fitness.fit2.height': 131, 'fitness.fit2.weight': 601},
                         {'id': 2, 'name': 'Faye Raker', 'someList': [], 'fitness.fit1': 201, 'fitness.fit2.height': 132, 'fitness.fit2.weight': 602},
                         {'id': 2, 'name': 'Faye Raker', 'someList': [], 'fitness.fit1': 201, 'fitness.fit2.height': 133, 'fitness.fit2.weight': 603},
                         {'id': 2, 'name': 'Faye Raker', 'someList': [], 'fitness.fit1': 202, 'fitness.fit2.height': 11, 'fitness.fit2.weight': 22},
                         {},
                         {'id': 3, 'name': 'AAA BBB'},
                         {'id': 4, 'name': 'AAA BBB'}
                         ]
        result = normalize_dicts(data, ["fitness", "fit2"])
        print(result)
        TestCase().assertListEqual(expected_list, result)


    def test_flatten_dict(self):
        data = [{
            "id": 1, "name": "Cole Volk", "fitness": [{"height": 130, "weight": 60}],
            "someDict": {"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}}
        },
        {
            "id": 2, "name": "Faye Raker", "fitness": [{"height": 130, "weight": 60}],
            "someDict": {"a": 201, "b": 202}, "someList": [1,2,3]
        }, ]
        expected_list = [
            {'id': 1, 'name': 'Cole Volk', "someDict.a": 101, "someDict.b": 102, "someDict.c.k1": 103, "someDict.c.k2": 104, 'fitness.height': 130, 'fitness.weight': 60},
            {'id': 2, 'name': 'Faye Raker', "someDict.a": 201, "someDict.b": 202, "someList": json.dumps([1,2,3]), 'fitness.height': 130, 'fitness.weight': 60}]
        result = normalize_dicts(data, ["fitness"], jsonify_lists=True)
        print(result)
        TestCase().assertListEqual(expected_list, result)


    def test_empty_path(self):
        data = [{
            "id": 1, "name": "Cole Volk", "fitness": [{"height": 130, "weight": 60}],
            "someDict": {"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}}
        },
        {
            "id": 2, "name": "Faye Raker", "fitness": [{"height": 130, "weight": 60}],
            "someDict": {"a": 201, "b": 202}, "someList": [1,2,3]
        }, ]
        expected_list = [
            {'id': 1, 'name': 'Cole Volk', 'fitness': json.dumps([{"height": 130, "weight": 60}]), "someDict.a": 101, "someDict.b": 102, "someDict.c.k1": 103, "someDict.c.k2": 104},
            {'id': 2, 'name': 'Faye Raker', 'fitness': json.dumps([{"height": 130, "weight": 60}]), "someDict.a": 201, "someDict.b": 202, "someList": json.dumps([1,2,3])}
        ]
        result = normalize_dicts(data, [], jsonify_lists=True)
        print(result)
        TestCase().assertListEqual(expected_list, result)


    def test_single_record_with_no_elems(self):
        # this shows that without a prototype, we can't rebuild exact columns in output dictionary
        data = [
        {
            "id": 2, "name": "Faye Raker", "fitness": [],
            "someList": [1]
        },
        ]
        expected_list = [
            {'id': 2, 'name': 'Faye Raker', 'someList': [1]}    # not sure if this makes sense, but this is how it works.
            # {'id': 2, 'name': 'Faye Raker', 'someList': [1], 'fitness.height': None, 'fitness.weight': None}  # current API doesn't allow this
        ]
        result = normalize_dicts(data, ["fitness"])
        print(result)
        TestCase().assertListEqual(expected_list, result)


    def test_jsonify_dicts(self):
        data = [{
            "id": 1, "name": "Cole Volk", "fitness": [{"height": 130, "weight": 60}],
            "someDict": {"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}}
        },
        {
            "id": 2, "name": "Faye Raker", "fitness": [{"height": 130, "weight": 60}],
            "someDict": {"a": 201, "b": 202}, "someList": [1, 2, 3]
        }, ]
        expected_list = [
            {'id': 1, 'name': 'Cole Volk', "someDict": json.dumps({"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}}),
             'fitness.height': 130, 'fitness.weight': 60},
            {'id': 2, 'name': 'Faye Raker', "someDict": json.dumps({"a": 201, "b": 202}), "someList": json.dumps([1, 2, 3]),
             'fitness.height': 130, 'fitness.weight': 60}]
        result = normalize_dicts(data, ["fitness"], jsonify_lists=True, jsonify_dicts=["someDict"])
        print(result)
        TestCase().assertListEqual(expected_list, result)


    def test_jsonify_dicts_2(self):
        data = [
            {
                "id": 1, "name": "John Smith",
                "pets": [
                    {"id": 101, "type": "cat", "name": "Kitty", "toys": [{"name": "toy1"}, {"name": "toy2"}], "someDict": {"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}}},
                    {"id": 102, "type": "dog", "name": "Barky", "toys": [{"name": "toy3"}], "someDict": {"other dict": 1122, "bbb": 202}}
                ]
            },
            {
                "id": 2, "name": "Sue Smith",
                "pets": [
                    {"id": 201, "type": "cat", "name": "Kitten", "toys": [{"name": "toy4"}, {"name": "toy5"}, {"name": "toy6"}]},
                    {"id": 202, "type": "dog", "name": "Fury", "toys": []}
                ]
            },
        ]

        expected_list = [
            {'id': 1, 'name': 'John Smith', 'pets.id': 101, 'pets.type': 'cat', 'pets.name': 'Kitty', 'pets.toys.name': 'toy1', 'pets.someDict': json.dumps({"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}})},
            {'id': 1, 'name': 'John Smith', 'pets.id': 101, 'pets.type': 'cat', 'pets.name': 'Kitty', 'pets.toys.name': 'toy2', 'pets.someDict': json.dumps({"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}})},
            {'id': 1, 'name': 'John Smith', 'pets.id': 102, 'pets.type': 'dog', 'pets.name': 'Barky', 'pets.toys.name': 'toy3', 'pets.someDict': json.dumps({"other dict": 1122, "bbb": 202})},
            {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy4'},
            {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy5'},
            {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy6'},
            {'id': 2, 'name': 'Sue Smith', 'pets.id': 202, 'pets.type': 'dog', 'pets.name': 'Fury'}]
        result = normalize_dicts(data, ["pets", "toys"], jsonify_dicts=["pets.someDict"])
        tc = TestCase()
        tc.maxDiff = 2000
        tc.assertListEqual(expected_list, result)



    def test_jsonify_dicts3(self):
        data = [{
            "id": 1, "name": "Cole Volk", "fitness": [{"height": 130, "weight": 60, "someDict": {"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}}}],
        },
        {
            "id": 2, "name": "Faye Raker", "fitness": [{"height": 130, "weight": 60,"someDict": {"a": 201, "b": 202}}],
            "someList": [1, 2, 3]
        }, ]
        expected_list = [
            {'id': 1, 'name': 'Cole Volk',
             'fitness.height': 130, 'fitness.weight': 60, "fitness.someDict": json.dumps({"a": 101, "b": 102, "c": {"k1": 103, "k2": 104}}),},
            {'id': 2, 'name': 'Faye Raker',
             'fitness.height': 130, 'fitness.weight': 60, "fitness.someDict": json.dumps({"a": 201, "b": 202}), "someList": json.dumps([1, 2, 3]),}]
        result = normalize_dicts(data, ["fitness"], jsonify_lists=True, jsonify_dicts=["fitness.someDict"])
        print(result)
        TestCase().assertListEqual(expected_list, result)
