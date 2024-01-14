from fastapi import APIRouter
from fastapi import status


router = APIRouter(
    prefix='/orders',
    tags=['Orders'],
)


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    description='Return all orders.',
)
def get_list_of_all_orders():
    return {'hello': 'world'}
