# bezalel

A library for ingesting data provided by paginated HTTP APIs


# Usage

## Basic use case

If you have to pull data from HTTP API that has an endpoint accepting parameters:

```
pageNumber=1,2,...
```

And returning JSON:

```json
{
    "pageCount": 5,
    "entities": [
      {"key":  "val1", ...},
      {"key":  "val2", ...},
      ...
    ]
}
```

Then you can iterate over all pages with following code:
```python
import requests
from bezalel import PaginatedApiIterator


for page in PaginatedApiIterator(requests.Session(), url=f"http://localhost:5000/page-api",
                                     request_page_number_param_name="pageNumber",
                                     response_page_count_field_name="pageCount",
                                     response_records_field_name="entities"):
    print(f"Page: {page}")
```

It will print:

```
Page: [{"key":  "val1", ...}, {"key":  "val2", ...}, ...]
Page: [{"key":  "val100", ...}, {"key":  "val101", ...}, ...]
Page: [{"key":  "val200", ...}, {"key":  "val201", ...}, ...]
...
```


## Grouping with `BufferingIterator`

If HTTP API doesn't allow you setting high number of records per page, use `BufferingIterator`.

```python
import requests
from bezalel import PaginatedApiIterator, BufferingIterator


for page in BufferingIterator(PaginatedApiIterator(requests.Session(), url=f"http://localhost:5000/page-api",
                                                       request_page_number_param_name="pageNumber",
                                                       response_page_count_field_name="pageCount",
                                                       response_records_field_name="entities"), buffer_size=2):
    print(f"Page: {page}")
```

It will combine multiple pages into one array, so that 
```
Page: [{"key":  "val1", ...}, {"key":  "val2", ...}, ..., {"key":  "val100", ...}, {"key":  "val101", ...}, ...]
Page: [{"key":  "val200", ...}, {"key":  "val201", ...}, ..., {"key":  "val300", ...}, {"key":  "val301", ...}, ...]
...
```

This is useful for fetching many records and storing them in fewer files (every file would be bigger). 


## Iterating over all records

TODO: this API will be improved in future release.

```python
import itertools
import requests
from bezalel import PaginatedApiIterator


all_elems = list(itertools.chain.from_iterable(PaginatedApiIterator(requests.Session(), url=f"https://your/api",
                                                   request_page_number_param_name="pageNumber",
                                                   response_page_count_field_name="pageCount",
                                                   response_records_field_name="entities"))):
print(f"len={len(all_elems)}: {all_elems}")
```

will print

```
len=12300: [{"key":  "val1", ...}, {"key":  "val2", ...}, ...]
```

## Helper function: `normalize_with_prototype()`

Normalize python dict, so that it has all the fields and only the fields specified in a prototype dict.

```python
from bezalel import normalize_with_prototype

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
```

would return

```python
result = {
    "id": 123,
    "name:": "John",
    "country": "Poland",
    "city": None,   # city was added
    "pets": [
        {"id": 101, "type": "dog", "name": "Barky"},
        {"id": 102, "type": "snail", "name": None}, # name was added
    ]
}
```


## Helper function: `normalize_dicts()`

Normalize list of nested python dicts to a list of one-level dicts.

Example:
```python
from bezalel import normalize_dicts

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

normalize_dicts(data, ["pets", "toys"])
```

would return:

```python
[{'id': 1, 'name': 'John Smith', 'pets.id': 101, 'pets.type': 'cat', 'pets.name': 'Kitty', 'pets.toys.name': 'toy1'},
 {'id': 1, 'name': 'John Smith', 'pets.id': 101, 'pets.type': 'cat', 'pets.name': 'Kitty', 'pets.toys.name': 'toy2'},
 {'id': 1, 'name': 'John Smith', 'pets.id': 102, 'pets.type': 'dog', 'pets.name': 'Barky', 'pets.toys.name': 'toy3'},
 {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy4'},
 {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy5'},
 {'id': 2, 'name': 'Sue Smith', 'pets.id': 201, 'pets.type': 'cat', 'pets.name': 'Kitten', 'pets.toys.name': 'toy6'},
 {'id': 2, 'name': 'Sue Smith', 'pets.id': 202, 'pets.type': 'dog', 'pets.name': 'Fury'}]
```

Presence of the last record can be controlled by flag `return_incomplete_records`. If `return_incomplete_records=False`
then last record in the example would not have been returned.

Additional options:
- jsonify_lists - when set to True, then if a list is encountered (not in main path), it is dumped as a JSON string.
- jsonify_dicts - list of paths for where to expect a dict. That dict will be then dumped as a JSON string.
