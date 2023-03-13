import requests
import logging


class PaginatedApiIterator:
    def __init__(self,
                 session: requests.Session,
                 url: str,
                 request_page_number_param_name: str,
                 # response_page_number_field_name: str,
                 response_page_count_field_name: str,
                 response_records_field_name: str,
                 extra_params: dict = {},
                 extra_headers: dict = {},
                 start_page_number_from_1=True,
                 http_method="GET"
                 ):
        self.logger = logging.getLogger(__name__)
        self._session = session
        self._http_method = http_method
        self._url = url
        self._request_page_number_param_name = request_page_number_param_name
        # self._response_page_number_field_name = response_page_number_field_name
        self._response_page_count_field_name = response_page_count_field_name
        self._response_records_field_name = response_records_field_name
        self._extra_params = extra_params
        self._request_headers = {
            # "Content-type": "application/json",
            "Accept": "application/json",
            **extra_headers
        }
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

        response = self._session.request(method=self._http_method, url=self._url, headers=self._request_headers,
                                     params={self._request_page_number_param_name: self.page_number, **self._extra_params})
        response.raise_for_status()

        response_json = response.json()
        page_count = response_json[self._response_page_count_field_name]

        self.logger.debug(
            f"Downloaded page {self.page_number} out of {page_count}. Items collected: {len(response_json[self._response_records_field_name])}")

        self.page_number += 1

        if (self._start_page_number_from_1 and self.page_number > page_count) or \
                (not self._start_page_number_from_1 and self.page_number >= page_count):
            self._completed = True

        return response_json[self._response_records_field_name]
