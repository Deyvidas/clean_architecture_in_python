import pytest
from fastapi import status
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from core.batch.models import Batch
from tests.api.conftest import CL_METHODS
from tests.api.conftest import Client
from tests.api.v1.conftest import create_batches_in_db


PREFIX = 'v1/batches'


@pytest.mark.parametrize(
    argnames='endpoint,method',
    argvalues=(
        pytest.param(f'{PREFIX}', Client.get, id=f'GET {repr(PREFIX)}'),
    ),
)
@pytest.mark.usefixtures('tables')
def test_existence_of_endpoint(endpoint: str, method: CL_METHODS):
    response = method(endpoint)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.usefixtures('tables')
def test_get_all_batches(session: Session):
    # TODO SOLVE PROBLEM WITH FASTAPI OUTPUT
    batches = create_batches_in_db(session, 3)
    response = Client.get(f'{PREFIX}')
    assert response.status_code == status.HTTP_200_OK
    assert response.content == TypeAdapter(list[Batch]).dump_json(batches)
