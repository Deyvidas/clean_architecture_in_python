from fastapi import APIRouter
from fastapi import status

from config.sqlalchemy_config import session_config
from core.order.models import OrderLine
from core.order.repo import OrderLineRepoSqlAlchemy


router = APIRouter(
    prefix='/orders',
    tags=['Orders'],
)


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    description='Return all orders.',
    response_model=list[OrderLine],
)
def get_list_of_all_orders():
    with session_config.session() as session:
        repo = OrderLineRepoSqlAlchemy(session)
        return repo.get()
