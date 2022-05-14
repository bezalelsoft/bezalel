import requests, json, time, os
import pandas as pd
import logging

def _write_file(df, out_path):
    logger = logging.getLogger(__name__)
    logger.info(f"Writing file {out_path} with {len(df)} records.")
    df.to_parquet(path=out_path, index=False)


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
        logger.info(state_response_json)
        state = state_response_json[response_state_field_name]
        logger.info(f"state: {state}")

    if state not in successful_states:
        raise Exception(f"Job failed with state {state}. Response {state_response_json}")

    return job_id


def paginated_api_ingestion(session: requests.Session,
                            url: str,
                            request_page_number_param_name: str,
                            response_page_number_field_name: str,
                            response_page_count_field_name: str,
                            response_records_field_name: str,
                            output_path: str,
                            extra_params: dict = {},
                            extra_headers: dict = {},
                            start_page_number_from_1=True,
                            pages_per_output_file: int = 1000):
    logger = logging.getLogger(__name__)
    logger.info(f"Downloading from {url} to {output_path}..")

    requestHeaders = {
        # "Content-type": "application/json",
        "Accept": "application/json",
        **extra_headers
    }

    per_file_df = None

    i = 1 if start_page_number_from_1 else 0
    df_per_file_counter = 0
    file_counter = 0
    were_column_names_printed = False

    while True:
        response = session.get(url, headers=requestHeaders, params={request_page_number_param_name: i, **extra_params})
        response.raise_for_status()

        response_json = response.json()
        page_number = response_json[
            response_page_number_field_name] if response_page_number_field_name is not None else i
        page_count = response_json[response_page_count_field_name]

        logger.info(
            f"Downloaded page {page_number} out of {page_count}. Items collected: {len(response_json[response_records_field_name])}")

        df = pd.json_normalize(response_json[response_records_field_name])
        if not were_column_names_printed:
            logger.info(f"Columns: {df.columns}")
            were_column_names_printed = True

        # to avoid ValueError: The truth value of a DataFrame is ambiguous.
        per_file_df = pd.concat([per_file_df, df]) if per_file_df is not None else df
        df_per_file_counter += 1

        if df_per_file_counter >= pages_per_output_file:
            _write_file(per_file_df, f"{output_path}/out_{file_counter}.parquet")
            per_file_df = None
            df_per_file_counter = 0
            file_counter += 1

        i += 1
        if start_page_number_from_1 and i > page_count:
            break
        if not start_page_number_from_1 and i >= page_count:
            break

    if per_file_df is not None:
        _write_file(per_file_df, f"{output_path}/out_{file_counter}.parquet")

    logger.info("All pages downloaded.")


def cursor_api_ingestion(session: requests.Session,
                         url: str,
                         request_cursor_param_name: str,
                         response_cursor_field_name: str,
                         response_records_field_name: str,
                         output_path: str,
                         extra_params: dict = {},
                         extra_headers: dict = {},
                         pages_per_output_file: int = 1000):
    logger = logging.getLogger(__name__)
    logger.info(f"Downloading from {url} to {output_path}..")

    requestHeaders = {
        # "Content-type": "application/json",
        "Accept": "application/json",
        **extra_headers
    }

    i = 1
    per_file_df = None
    df_per_file_counter = 0
    file_counter = 0
    were_column_names_printed = False

    params = {**extra_params}

    while True:
        response = session.get(url, headers=requestHeaders, params=params)
        response.raise_for_status()

        response_json = response.json()
        params[request_cursor_param_name] = response_json.get(response_cursor_field_name)

        logger.info(
            f"Downloaded page {i}. Items collected: {len(response_json[response_records_field_name])}")

        df = pd.json_normalize(response_json[response_records_field_name])
        if not were_column_names_printed:
            logger.info(f"Columns: {df.columns}")
            were_column_names_printed = True

        # to avoid ValueError: The truth value of a DataFrame is ambiguous.
        per_file_df = pd.concat([per_file_df, df]) if per_file_df is not None else df
        df_per_file_counter += 1

        if df_per_file_counter >= pages_per_output_file:
            _write_file(per_file_df, f"{output_path}/out_{file_counter}.parquet")
            per_file_df = None
            df_per_file_counter = 0
            file_counter += 1
        if response_cursor_field_name not in response_json:
            break

        i += 1

    if per_file_df is not None:
        _write_file(per_file_df, f"{output_path}/out_{file_counter}.parquet")

    logger.info("All pages downloaded.")
