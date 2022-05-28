import requests
import logging


class CursorApiIterator:
    def __init__(self, session: requests.Session,
                         url: str,
                         request_cursor_param_name: str,
                         response_cursor_field_name: str,
                         response_records_field_name: str,
                         extra_params: dict = {},
                         extra_headers: dict = {}):
        self.logger = logging.getLogger(__name__)
        self._session = session
        self._url = url
        self._request_cursor_param_name = request_cursor_param_name
        self._response_cursor_field_name = response_cursor_field_name
        self._response_records_field_name = response_records_field_name
        self._extra_params = extra_params
        self._request_headers = {
            # "Content-type": "application/json",
            "Accept": "application/json",
            **extra_headers
        }
        self._completed = False
        self._next_cursor = None
        self.page_number = 1

    def __iter__(self):
        self.logger.debug(f"Downloading from {self._url}")
        self._completed = False
        self._next_cursor = None
        self.page_number = 1
        return self

    def __next__(self):
        if self._completed:
            raise StopIteration
        params = {**self._extra_params}
        params[self._request_cursor_param_name] = self._next_cursor

        response = self._session.get(self._url, headers=self._request_headers, params=params)
        response.raise_for_status()

        response_json = response.json()

        self._next_cursor = response_json.get(self._response_cursor_field_name)
        self._completed = self._next_cursor is None

        self.logger.debug(
            f"Downloaded page {self.page_number}. Items collected: {len(response_json[self._response_records_field_name])}")
        self.page_number += 1

        return response_json[self._response_records_field_name]
