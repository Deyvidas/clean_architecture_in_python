from sqlalchemy.orm.session import Session

from core.order.models import OrderLine
from core.order.repo import OrderLineRepoSqlAlchemy


def test_write_and_read_using_repository(session: Session):
    repo = OrderLineRepoSqlAlchemy(session)
    model = OrderLine(product_name='SMALL-BAD', ordered_quantity=5)

    added = repo.add(model)
    received = repo.get(id=model.id)

    assert len(received) == 1
    assert isinstance(received := received[0], OrderLine)

    assert added.id == received.id
    assert added.product_name == received.product_name
    assert added.ordered_quantity == received.ordered_quantity
