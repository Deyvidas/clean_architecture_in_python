import pytest
from fastapi.testclient import TestClient

from api.v1.root import api_v1


@pytest.fixture
def client() -> TestClient:
    return TestClient(api_v1)
