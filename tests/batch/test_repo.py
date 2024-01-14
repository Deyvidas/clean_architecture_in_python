import pytest
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.batch.models import Batch
from core.batch.orm import BatchOrm
from core.batch.repo import BatchRepoSqlAlchemy
from tests.factories.batch import BatchFactory
from tests.factories.order import OrderLineFactory


@pytest.mark.usefixtures('tables')
def test_add(session: Session, batch_factory: BatchFactory):
    repo = BatchRepoSqlAlchemy(session)
    model = batch_factory.generate_one()

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
def test_get(session: Session, batch_factory: BatchFactory):
    repo = BatchRepoSqlAlchemy(session)
    model = batch_factory.generate_one()
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
def test_create_with_allocations(
    session: Session,
    batch_factory: BatchFactory,
    order_factory: OrderLineFactory,
):
    repo = BatchRepoSqlAlchemy(session)
    batch = batch_factory.generate_one()
    orders = order_factory.generate_many(2, product_name=batch.product_name)

    batch.allocate(orders[0])
    batch.allocate(orders[1])
    repo.add(batch)
    session.commit()

    received = repo.get(id=batch.id)
    assert len(received) == 1
    assert isinstance(first := received[0], Batch)
    assert first.allocations == orders
