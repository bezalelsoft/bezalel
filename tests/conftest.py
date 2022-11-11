import pytest
from multiprocessing import Process
from mock_service import run_uvicorn_server


@pytest.fixture(scope="module")
def mock_service():
    proc = Process(target=run_uvicorn_server, args=(), daemon=True)
    proc.start()
    yield proc
    proc.kill()  # Cleanup after test
