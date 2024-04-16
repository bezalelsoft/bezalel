import requests
import logging
import typing as t


class CursorApiIterator:
    def __init__(self,
                 session: requests.Session,
                 url: str,
                 method: str,
                 response_cursor_field_name: str,
                 response_records_field_name: str,
                 request_cursor_param_name: t.Optional[str] = None,
                 request_cursor_field_name: t.Optional[str] = None,
                 extra_params: t.Optional[dict] = None,
                 extra_data: t.Optional[dict] = None,
                 extra_headers: t.Optional[dict] = None,
                 empty_data_on_next_cursor: bool=False,
                 payload_handler=None):
        """

        :param session: requests.Session object (you can set session.auth = (user, passwd) for authentication)
        :param url: url to call
        :param method: get or post
        :param response_cursor_field_name:
        :param response_records_field_name:
        :param request_cursor_param_name:
        :param request_cursor_field_name:
        :param extra_params: URL params
        :param extra_data: request payload params
        :param extra_headers:
        :param empty_data_on_next_cursor: Flase
        :param payload_handler: a function that is called just after fetching next page. Takes dict as a param.
        """
        self.logger = logging.getLogger(__name__)
        self._session = session
        self._url = url
        self._method = method.upper()
        self._request_cursor_param_name = request_cursor_param_name
        self._request_cursor_field_name = request_cursor_field_name
        self._response_cursor_field_name = response_cursor_field_name
        self._response_records_field_name = response_records_field_name
        self._extra_params = extra_params
        self._extra_data = extra_data
        self._request_headers = {
            "Accept": "application/json",
        }
        if self._request_cursor_field_name:
            self._request_headers["Content-type"] = "application/json"
        if extra_headers:
            for k, v in extra_headers.items():
                self._request_headers[k] = v
        self._empty_data_on_next_cursor = empty_data_on_next_cursor
        self._payload_handler = payload_handler
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
        if self._extra_params or self._request_cursor_param_name:
            params = {}
            if self._extra_params:
                params = {**self._extra_params}
            params[self._request_cursor_param_name] = self._next_cursor
        else:
            params = None

        if self._extra_data or self._request_cursor_field_name:
            data = {}

            if self._extra_data and (not self._empty_data_on_next_cursor or not self._next_cursor):
                data = {**self._extra_data}

            if self._request_cursor_field_name and self._next_cursor:
                data[self._request_cursor_field_name] = self._next_cursor
            data = data.dict()
        else:
            data = None

        response = self._session.request(method=self._method, url=self._url, headers=self._request_headers, params=params, json=data)
        response.raise_for_status()

        response_json = response.json()

        if self._payload_handler:
            self._payload_handler(response_json)

        if self._response_records_field_name not in response_json.keys():
            raise Exception(f"Failed to get field '{self._response_records_field_name}' from response {response_json}. Request params: '{params}' data: '{data}'")

        self._next_cursor = response_json.get(self._response_cursor_field_name)
        self._completed = not self._next_cursor
        self.logger.debug(
            f"Downloaded page {self.page_number}. Items collected: {len(response_json[self._response_records_field_name])}")
        self.page_number += 1

        return response_json[self._response_records_field_name]
