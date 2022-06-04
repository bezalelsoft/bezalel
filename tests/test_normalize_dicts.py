from pprint import pprint

if __name__ == '__main__':
    # example 1:
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
    pprint(normalize_dicts(data, ["pets", "toys"]), sort_dicts=False)

    print("HHHHHHHHHHHHHHHHHHHHHHHHHHH")

    # This works fine:
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
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHH")
    pprint(normalize_dicts(data, ["fitness"]), sort_dicts=False)

    # This doesn't work
    data = [{
        "id": 1, "name": "Cole Volk", "fitness": [{"height": 130, "weight": 60}],
        "someList": []
    },
    {
        "id": 2, "name": "Faye Raker", "fitness": [{"height": 130, "weight": 60}],
        "someList": []
    }, ]
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHH")
    pprint(normalize_dicts(data, ["fitness"]), sort_dicts=False)

    # 2 level
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
    # {"id": 4, "name": "AAA BBB", "fitness": "not-a-list"}
    ]
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHH")
    pprint(normalize_dicts(data, ["fitness", "fit2"]), sort_dicts=False)
