import pytest
from fastapi.testclient import TestClient

from intent_detector_service.app import app


@pytest.fixture()
def app_client() -> TestClient:
    client = TestClient(app)
    return client
