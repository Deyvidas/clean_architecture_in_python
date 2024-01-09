import pytest
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.order.models import OrderLine
from core.order.orm import OrderLineOrm
from core.order.repo import OrderLineRepoSqlAlchemy
from tests.order.conftest import order_data


@pytest.mark.usefixtures('tables')
def test_repository_add(session: Session):
    repo = OrderLineRepoSqlAlchemy(session)
    model = OrderLine(**order_data().asdict())

    added = repo.add(model)
    assert isinstance(added, OrderLine)
    assert added.id == model.id
    assert added.product_name == model.product_name
    assert added.ordered_quantity == model.ordered_quantity

    stmt = select(OrderLineOrm).filter_by(id=model.id)
    orm = session.scalars(stmt).unique().all()
    assert len(orm) == 1
    assert isinstance(orm := orm[0], OrderLineOrm)

    received = TypeAdapter(OrderLine).validate_python(orm)
    assert added.id == received.id
    assert added.product_name == received.product_name
    assert added.ordered_quantity == received.ordered_quantity


@pytest.mark.usefixtures('tables')
def test_repository_get(session: Session):
    repo = OrderLineRepoSqlAlchemy(session)
    model = OrderLine(**order_data().asdict())
    repo.add(model)

    received = repo.get(id=model.id)
    assert len(received) == 1
    assert isinstance(received := received[0], OrderLine)
    assert received.id == model.id
    assert received.product_name == model.product_name
    assert received.ordered_quantity == model.ordered_quantity
