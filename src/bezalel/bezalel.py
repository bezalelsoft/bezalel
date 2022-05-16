import requests
import time
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
                 start_page_number_from_1=True
                 ):
        self.logger = logging.getLogger(__name__)
        self._session = session
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

        response = self._session.get(self._url, headers=self._request_headers,
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


def prepare_job(session: requests.Session, url: str,
                response_job_id_field_name: str,
                response_state_field_name: str,
                successful_states: [str],
                waiting_states: [str],
                extra_params: dict = {}, extra_headers: dict = {},
                wait_delay_seconds=5):
    logger = logging.getLogger(__name__)
    requestHeaders = {
        "Content-type": "application/json",
        "Accept": "application/json",
        **extra_headers
    }
    response = session.post(url, headers=requestHeaders, json={**extra_params})
    response.raise_for_status()

    job_id = response.json()[response_job_id_field_name]
    state = waiting_states[0]
    state_response_json = None
    while state in waiting_states:
        time.sleep(wait_delay_seconds)
        state_response = session.get(f"{url}/{job_id}", headers=requestHeaders)
        state_response_json = state_response.json()
        logger.debug(state_response_json)
        state = state_response_json[response_state_field_name]
        logger.debug(f"state: {state}")

    if state not in successful_states:
        raise Exception(f"Job failed with state {state}. Response {state_response_json}")

    return job_id

