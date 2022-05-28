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

