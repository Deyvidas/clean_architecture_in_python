from fastapi import APIRouter
from fastapi import status


router = APIRouter(
    prefix='/batches',
    tags=['Batches'],
)


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    description='Return all batches.',
)
def get_list_of_all_batches():
    return {'hello': 'world'}
