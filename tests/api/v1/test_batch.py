from fastapi import status
from fastapi.testclient import TestClient


PREFIX = 'v1/batches'


class TestStatusCode:
    def test_GET(self, client: TestClient):
        response = client.get(f'{PREFIX}')
        assert response.status_code == status.HTTP_200_OK
