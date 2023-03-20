import logging
import math
import requests

from .dict_utils import *


class PaginatedApiIterator:

    def __init__(self,
                 session: requests.Session,
                 url: str,
                 request_page_number_param_name: str,
                 # response_page_number_field_name: str,
                 response_records_field_name: str,
                 response_page_count_field_name: Optional[str]=None,
                 response_record_count_field_name: Optional[str]=None,
                 records_per_page: Optional[int]=None,
                 extra_params: dict = None,
                 extra_headers: dict = None,
                 extra_data_fields: dict = None,
                 start_page_number_from_1=True,
                 http_method="GET",
                 request_page_number_location: str = "params"
                 ):
        self.logger = logging.getLogger(__name__)
        self._session = session
        self._http_method = http_method
        self._url = url
        self._request_page_number_param_name = request_page_number_param_name
        self._request_page_number_location = request_page_number_location
        # self._response_page_number_field_name = response_page_number_field_name
        if response_page_count_field_name is None and response_record_count_field_name is None or response_page_count_field_name is not None and response_record_count_field_name is not None:
            raise Exception("Exactly one of response_page_count_field_name, response_record_count_field_name must be provided.")
        self._response_page_count_field_name = response_page_count_field_name
        self._response_record_count_field_name = response_record_count_field_name
        if response_record_count_field_name is not None and records_per_page is None:
            raise Exception("If response_record_count_field_name is provided then records_per_page must be also provided.")
        self._records_per_page = records_per_page

        self._response_records_field_name = response_records_field_name
        self._extra_params = extra_params
        if extra_headers:
            self._request_headers = {
                # "Content-type": "application/json",
                "Accept": "application/json",
                **extra_headers
            }
        else:
            self._request_headers = {
                # "Content-type": "application/json",
                "Accept": "application/json"
            }
        self._extra_data_fields = extra_data_fields
        self._start_page_number_from_1 = start_page_number_from_1
        self.page_number = 1 if self._start_page_number_from_1 else 0
        self._completed = False
    def __iter__(self):
        self.logger.debug(f"Downloading from {self._url}")
        self.page_number = 1 if self._start_page_number_from_1 else 0
        self._completed = False
        return self

    def __next__(self):
        if self._completed:
            raise StopIteration

        request_params = None
        if self._extra_params is not None:
            request_params = self._extra_params.copy()

        request_data = None
        if self._extra_data_fields is not None:
            request_data = self._extra_data_fields.copy()

        if self._request_page_number_location == "params":
            if request_params is None:
                request_params = {}
            request_params[self._request_page_number_param_name] = self.page_number
        elif self._request_page_number_location == "data":
            if request_data is None:
                request_data = {}
            dict_set(request_data, self._request_page_number_param_name, self.page_number)
        else:
            raise Exception(f"Wrong parameter value request_page_number_location={self._request_page_number_location}")

        response = self._session.request(method=self._http_method, url=self._url, headers=self._request_headers,
                                         params=request_params, json=request_data)
        response.raise_for_status()

        response_json = response.json()
        if self._response_page_count_field_name is not None:
            page_count = dict_get(response_json, self._response_page_count_field_name)
        else:
            records_count = dict_get(response_json, self._response_record_count_field_name)
            page_count = math.ceil(records_count/self._records_per_page)

        records = dict_get(response_json, self._response_records_field_name, [])

        self.logger.debug(f"Downloaded page {self.page_number} out of {page_count}. Items collected: {len(records)}")

        self.page_number += 1

        if (self._start_page_number_from_1 and self.page_number > page_count) or \
                (not self._start_page_number_from_1 and self.page_number >= page_count):
            self._completed = True

        return records
