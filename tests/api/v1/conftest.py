from random import randint
from typing import Any

from sqlalchemy.orm import Session

from core.batch.models import Batch
from core.batch.repo import BatchRepoSqlAlchemy
from core.order.models import OrderLine
from core.order.repo import OrderLineRepoSqlAlchemy
from tests.factories.batch import BatchFactory
from tests.factories.order import OrderLineFactory


def create_orders_in_db(
    session: Session,
    qnt: int,
    **kwargs: Any,
) -> list[OrderLine]:
    repo = OrderLineRepoSqlAlchemy(session)
    orders = OrderLineFactory().generate_many(qnt, **kwargs)
    orders = [repo.add(o) for o in orders]
    session.commit()
    return orders


def create_batches_in_db(
    session: Session,
    qnt: int,
    **kwargs: Any,
) -> list[Batch]:
    repo = BatchRepoSqlAlchemy(session)
    batches = BatchFactory().generate_many(qnt, **kwargs)

    for batch in batches:
        orders = OrderLineFactory().generate_many(
            randint(0, 5),
            product_name=batch.product_name,
        )
        [batch.allocate(o) for o in orders]

    batches = [repo.add(b) for b in batches]
    session.commit()
    return batches
