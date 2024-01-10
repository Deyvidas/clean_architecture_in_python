from datetime import date
from datetime import timedelta

import pytest

from core.batch.models import Batch
from core.batch.models import allocate
from core.order.models import OrderLine
from core.utils.exceptions import OutOfStock
from tests.batch.conftest import batch_data
from tests.order.conftest import order_data


today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=10)


def test_priority_to_goods_in_stock():
    BatchDataInStock = batch_data(estimated_arrival_date=None)
    BatchDataOrdered = batch_data(estimated_arrival_date=today)
    OrderData = order_data()

    batch_in_stock = Batch(**BatchDataInStock.asdict())
    batch_ordered = Batch(**BatchDataOrdered.asdict())
    order = OrderLine(**OrderData.asdict())

    allocate(order, [batch_ordered, batch_in_stock])

    assert batch_in_stock.allocations == [order]
    assert batch_in_stock.allocated_quantity == OrderData.ordered_quantity
    assert batch_in_stock.available_quantity == (
        BatchDataInStock.purchased_quantity - OrderData.ordered_quantity
    )

    assert batch_ordered.allocations == list()
    assert batch_ordered.allocated_quantity == 0
    assert batch_ordered.available_quantity == (
        BatchDataOrdered.purchased_quantity
    )


def test_priority_to_earlier():
    BatchDataEarlier = batch_data(estimated_arrival_date=today)
    BatchDataLater = batch_data(estimated_arrival_date=tomorrow)
    OrderData = order_data()

    batch_earlier = Batch(**BatchDataEarlier.asdict())
    batch_later = Batch(**BatchDataLater.asdict())
    order = OrderLine(**OrderData.asdict())

    allocate(order, [batch_later, batch_earlier])

    assert batch_earlier.allocations == [order]
    assert batch_earlier.allocated_quantity == OrderData.ordered_quantity
    assert batch_earlier.available_quantity == (
        BatchDataEarlier.purchased_quantity - OrderData.ordered_quantity
    )

    assert batch_later.allocations == list()
    assert batch_later.allocated_quantity == 0
    assert batch_later.available_quantity == BatchDataLater.purchased_quantity


def test_allocate_return_id_of_batch_where_order_is_allocated():
    BatchDataInStock = batch_data(estimated_arrival_date=None)
    BatchDataOrdered = batch_data(estimated_arrival_date=later)
    OrderData = order_data()

    batch_in_stock = Batch(**BatchDataInStock.asdict())
    batch_ordered = Batch(**BatchDataOrdered.asdict())
    order = OrderLine(**OrderData.asdict())

    allocated_in_batch_id = allocate(order, [batch_ordered, batch_in_stock])

    assert allocated_in_batch_id == BatchDataInStock.id


def test_raises_out_of_stock_if_ordered_product_not_ordered_and_not_in_stock():
    BatchDataInStock = batch_data(estimated_arrival_date=None)
    BatchDataOrdered = batch_data(estimated_arrival_date=later)
    OrderAllInStock = order_data(
        ordered_quantity=BatchDataInStock.purchased_quantity,
    )
    OrderAllOrdered = order_data(
        ordered_quantity=BatchDataOrdered.purchased_quantity,
    )
    OrderOutOfStock = order_data()

    batch_in_stock = Batch(**BatchDataInStock.asdict())
    batch_ordered = Batch(**BatchDataOrdered.asdict())
    order_all_in_stock = OrderLine(**OrderAllInStock.asdict())
    order_all_ordered = OrderLine(**OrderAllOrdered.asdict())
    order_out_of_stock = OrderLine(**OrderOutOfStock.asdict())

    allocate(order_all_in_stock, [batch_ordered, batch_in_stock])
    allocate(order_all_ordered, [batch_in_stock, batch_ordered])

    with pytest.raises(OutOfStock, match=order_out_of_stock.product_name):
        allocate(order_out_of_stock, [batch_ordered, batch_in_stock])
