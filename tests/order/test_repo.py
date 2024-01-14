import pytest
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.order.models import OrderLine
from core.order.orm import OrderLineOrm
from core.order.repo import OrderLineRepoSqlAlchemy
from tests.factories.order import OrderLineFactory


@pytest.mark.usefixtures('tables')
def test_add(session: Session, order_factory: OrderLineFactory):
    repo = OrderLineRepoSqlAlchemy(session)
    model = order_factory.generate_one()

    added = repo.add(model)
    session.commit()
    assert isinstance(added, OrderLine)
    assert added.id == model.id
    assert added.product_name == model.product_name
    assert added.ordered_quantity == model.ordered_quantity

    stmt = select(OrderLineOrm).filter_by(id=model.id)
    orm = session.scalars(stmt).unique().all()
    assert len(orm) == 1
    assert isinstance(first := orm[0], OrderLineOrm)

    received = TypeAdapter(OrderLine).validate_python(first)
    assert added.id == received.id
    assert added.product_name == received.product_name
    assert added.ordered_quantity == received.ordered_quantity


@pytest.mark.usefixtures('tables')
def test_get(session: Session, order_factory: OrderLineFactory):
    repo = OrderLineRepoSqlAlchemy(session)
    model = order_factory.generate_one()
    repo.add(model)
    session.commit()

    received = repo.get(id=model.id)
    assert len(received) == 1
    assert isinstance(first := received[0], OrderLine)
    assert first.id == model.id
    assert first.product_name == model.product_name
    assert first.ordered_quantity == model.ordered_quantity
