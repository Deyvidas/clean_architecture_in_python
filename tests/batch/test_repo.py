import pytest
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.batch.models import Batch
from core.batch.orm import BatchOrm
from core.batch.repo import BatchRepoSqlAlchemy
from core.order.models import OrderLine
from tests.batch.conftest import batch_data
from tests.order.conftest import order_data


@pytest.mark.usefixtures('tables')
def test_add(session: Session):
    repo = BatchRepoSqlAlchemy(session, Batch, BatchOrm)
    model = Batch(**batch_data().asdict())

    added = repo.add(model)
    session.commit()
    assert isinstance(added, Batch)
    assert added.id == model.id
    assert added.product_name == model.product_name
    assert added.purchased_quantity == model.purchased_quantity
    assert added.estimated_arrival_date == model.estimated_arrival_date

    stmt = select(BatchOrm).filter_by(id=model.id)
    orm = session.scalars(stmt).unique().all()
    assert len(orm) == 1
    assert isinstance(first := orm[0], BatchOrm)

    received = TypeAdapter(Batch).validate_python(first)
    assert added.id == received.id
    assert added.product_name == received.product_name
    assert added.purchased_quantity == received.purchased_quantity
    assert added.estimated_arrival_date == received.estimated_arrival_date


@pytest.mark.usefixtures('tables')
def test_get(session: Session):
    repo = BatchRepoSqlAlchemy(session, Batch, BatchOrm)
    model = Batch(**batch_data().asdict())
    repo.add(model)
    session.commit()

    received = repo.get(id=model.id)
    assert len(received) == 1
    assert isinstance(first := received[0], Batch)
    assert first.id == model.id
    assert first.product_name == model.product_name
    assert first.purchased_quantity == model.purchased_quantity
    assert first.estimated_arrival_date == model.estimated_arrival_date


@pytest.mark.usefixtures('tables')
def test_create_with_allocations(session: Session):
    repo = BatchRepoSqlAlchemy(session, Batch, BatchOrm)
    batch = Batch(**batch_data().asdict())
    order1 = OrderLine(**order_data().asdict())
    order2 = OrderLine(**order_data().asdict())

    batch.allocate(order1)
    batch.allocate(order2)
    repo.add(batch)
    session.commit()

    received = repo.get(id=batch.id)
    assert len(received) == 1
    assert isinstance(first := received[0], Batch)
    assert first.allocations == [order1, order2]
