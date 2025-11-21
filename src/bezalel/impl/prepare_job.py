import requests
import time
import logging


def prepare_job(session: requests.Session, url: str,
                response_job_id_field_name: str,
                response_state_field_name: str,
                successful_states: [str],
                waiting_states: [str],
                extra_params: dict = {}, extra_headers: dict = {},
                wait_delay_seconds=5,
                timeout=(10, 60),
                ):
    logger = logging.getLogger(__name__)
    requestHeaders = {
        "Content-type": "application/json",
        "Accept": "application/json",
        **extra_headers
    }
    response = session.post(url, headers=requestHeaders, json={**extra_params}, timeout=timeout)
    response.raise_for_status()

    job_id = response.json()[response_job_id_field_name]
    state = waiting_states[0]
    state_response_json = None
    while state in waiting_states:
        time.sleep(wait_delay_seconds)
        state_response = session.get(f"{url}/{job_id}", headers=requestHeaders, timeout=timeout)
        state_response_json = state_response.json()
        logger.debug(state_response_json)
        state = state_response_json[response_state_field_name]
        logger.debug(f"state: {state}")

    if state not in successful_states:
        raise Exception(f"Job failed with state {state}. Response {state_response_json}")

    return job_id

