from datetime import date
from datetime import timedelta

import pytest

from core.batch.models import allocate
from core.utils.exceptions import OutOfStock
from tests.factories.batch import BatchFactory
from tests.factories.order import OrderLineFactory


today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=10)


def test_priority_to_goods_in_stock(
    batch_factory: BatchFactory,
    order_factory: OrderLineFactory,
):
    batch_in_stock = batch_factory.generate_one(
        estimated_arrival_date=None,
    )
    batch_ordered = batch_factory.generate_one(
        estimated_arrival_date=today,
        product_name=batch_in_stock.product_name,
    )
    order = order_factory.generate_one(
        product_name=batch_in_stock.product_name,
    )

    allocate(order, [batch_ordered, batch_in_stock])

    assert batch_in_stock.allocations == [order]
    assert batch_in_stock.allocated_quantity == order.ordered_quantity
    assert batch_in_stock.available_quantity == (
        batch_in_stock.purchased_quantity - order.ordered_quantity
    )

    assert batch_ordered.allocations == list()
    assert batch_ordered.allocated_quantity == 0
    assert batch_ordered.available_quantity == batch_ordered.purchased_quantity


def test_priority_to_earlier(
    batch_factory: BatchFactory,
    order_factory: OrderLineFactory,
):
    batch_earlier = batch_factory.generate_one(
        estimated_arrival_date=today,
    )
    batch_later = batch_factory.generate_one(
        estimated_arrival_date=tomorrow,
        product_name=batch_earlier.product_name,
    )
    order = order_factory.generate_one(
        product_name=batch_earlier.product_name,
    )

    allocate(order, [batch_later, batch_earlier])

    assert batch_earlier.allocations == [order]
    assert batch_earlier.allocated_quantity == order.ordered_quantity
    assert batch_earlier.available_quantity == (
        batch_earlier.purchased_quantity - order.ordered_quantity
    )

    assert batch_later.allocations == list()
    assert batch_later.allocated_quantity == 0
    assert batch_later.available_quantity == batch_later.purchased_quantity


def test_allocate_return_id_of_batch_where_order_is_allocated(
    batch_factory: BatchFactory,
    order_factory: OrderLineFactory,
):
    batch_in_stock = batch_factory.generate_one(
        estimated_arrival_date=None,
    )
    batch_ordered = batch_factory.generate_one(
        estimated_arrival_date=later,
        product_name=batch_in_stock.product_name,
    )
    order = order_factory.generate_one(
        product_name=batch_in_stock.product_name,
    )

    allocated_in_batch_id = allocate(order, [batch_ordered, batch_in_stock])

    assert allocated_in_batch_id == batch_in_stock.id


def test_raises_out_of_stock_if_ordered_product_not_ordered_and_not_in_stock(
    batch_factory: BatchFactory,
    order_factory: OrderLineFactory,
):
    batch_in_stock = batch_factory.generate_one(
        estimated_arrival_date=None,
    )
    batch_ordered = batch_factory.generate_one(
        estimated_arrival_date=later,
        product_name=batch_in_stock.product_name,
    )
    order_all_in_stock = order_factory.generate_one(
        ordered_quantity=batch_in_stock.purchased_quantity,
        product_name=batch_in_stock.product_name,
    )
    order_all_ordered = order_factory.generate_one(
        ordered_quantity=batch_ordered.purchased_quantity,
        product_name=batch_in_stock.product_name,
    )
    order_out_of_stock = order_factory.generate_one(
        product_name=batch_in_stock.product_name,
    )

    allocate(order_all_in_stock, [batch_ordered, batch_in_stock])
    allocate(order_all_ordered, [batch_in_stock, batch_ordered])

    with pytest.raises(OutOfStock, match=order_out_of_stock.product_name):
        allocate(order_out_of_stock, [batch_ordered, batch_in_stock])
