from fastapi import APIRouter
from fastapi import status

from config.sqlalchemy_config import session_config
from core.batch.models import Batch
from core.batch.repo import BatchRepoSqlAlchemy


router = APIRouter(
    prefix='/batches',
    tags=['Batches'],
)


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    description='Return all batches.',
    response_model=list[Batch],
)
def get_list_of_all_batches():
    with session_config.session() as session:
        repo = BatchRepoSqlAlchemy(session)
        return repo.get()
