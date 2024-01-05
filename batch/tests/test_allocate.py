from datetime import date
from datetime import timedelta

from batch.models import allocate
from batch.models import Batch
from batch.tests.utils import batch_data
from batch.tests.utils import order_data
from order.models import OrderLine


today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=10)


def test_priority_to_goods_in_stock():
    BatchDataInStock = batch_data(estimated_arrival_date=None)
    BatchDataInTransit = batch_data(estimated_arrival_date=today)
    OrderData = order_data()

    batch_in_stock = Batch(**BatchDataInStock.asdict())
    batch_in_transit = Batch(**BatchDataInTransit.asdict())
    order = OrderLine(**OrderData.asdict())

    allocate(order, [batch_in_transit, batch_in_stock])

    assert batch_in_stock.allocations == set([order])
    assert batch_in_stock.allocated_quantity == OrderData.ordered_quantity
    assert batch_in_stock.available_quantity == (
        BatchDataInStock.purchased_quantity - OrderData.ordered_quantity
    )

    assert batch_in_transit.allocations == set()
    assert batch_in_transit.allocated_quantity == 0
    assert batch_in_transit.available_quantity == (
        BatchDataInTransit.purchased_quantity
    )


def test_priority_to_earlier():
    BatchDataEarlier = batch_data(estimated_arrival_date=today)
    BatchDataLater = batch_data(estimated_arrival_date=tomorrow)
    OrderData = order_data()

    batch_earlier = Batch(**BatchDataEarlier.asdict())
    batch_later = Batch(**BatchDataLater.asdict())
    order = OrderLine(**OrderData.asdict())

    allocate(order, [batch_later, batch_earlier])

    assert batch_earlier.allocations == set([order])
    assert batch_earlier.allocated_quantity == OrderData.ordered_quantity
    assert batch_earlier.available_quantity == (
        BatchDataEarlier.purchased_quantity - OrderData.ordered_quantity
    )

    assert batch_later.allocations == set()
    assert batch_later.allocated_quantity == 0
    assert batch_later.available_quantity == BatchDataLater.purchased_quantity


def test_allocate_return_id_of_batch_where_order_is_allocated():
    BatchDataInStock = batch_data(estimated_arrival_date=None)
    BatchDataInTransit = batch_data(estimated_arrival_date=later)
    OrderData = order_data()

    batch_in_stock = Batch(**BatchDataInStock.asdict())
    batch_in_transit = Batch(**BatchDataInTransit.asdict())
    order = OrderLine(**OrderData.asdict())

    allocated_in_batch_id = allocate(order, [batch_in_transit, batch_in_stock])

    assert allocated_in_batch_id == BatchDataInStock.id
