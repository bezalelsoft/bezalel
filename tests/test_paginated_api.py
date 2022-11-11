import sys, os

print(f"sys.path: {sys.path}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")

import requests
from bezalel import PaginatedApiIterator, BufferingIterator
from unittest import TestCase
from mock_service import generate_pages


def test_PaginatedApiIterator(mock_service):
    pages = []
    for page in PaginatedApiIterator(requests.Session(), url=f"http://localhost:5000/page-api",
                                     request_page_number_param_name="pageNumber",
                                     response_page_count_field_name="pageCount",
                                     response_records_field_name="entities"):
        pages.append(page)

    exptected_pages = generate_pages()

    TestCase().assertListEqual(exptected_pages, pages)


def test_BufferingIterator(mock_service):
    pages = []
    for page in BufferingIterator(PaginatedApiIterator(requests.Session(), url=f"http://localhost:5000/page-api",
                                                       request_page_number_param_name="pageNumber",
                                                       response_page_count_field_name="pageCount",
                                                       response_records_field_name="entities"), buffer_size=2):
        pages.append(page)
    # print(pages)

    exptected_pages = [[{'key1': 'val', 'r': 0, 'rInPage': 0},
                        {'key1': 'val', 'r': 1, 'rInPage': 1},
                        {'key1': 'val', 'r': 2, 'rInPage': 2},
                        {'key1': 'val', 'r': 3, 'rInPage': 0},
                        {'key1': 'val', 'r': 4, 'rInPage': 1},
                        {'key1': 'val', 'r': 5, 'rInPage': 2}],

                       [{'key1': 'val', 'r': 6, 'rInPage': 0},
                        {'key1': 'val', 'r': 7, 'rInPage': 1},
                        {'key1': 'val', 'r': 8, 'rInPage': 2},
                        {'key1': 'val', 'r': 9, 'rInPage': 0},
                        {'key1': 'val', 'r': 10, 'rInPage': 1},
                        {'key1': 'val', 'r': 11, 'rInPage': 2}]
                       ]

    TestCase().assertListEqual(exptected_pages, pages)
