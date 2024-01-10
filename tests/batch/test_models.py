import pytest

from core.batch.models import Batch
from core.order.models import OrderLine
from tests.batch.conftest import batch_data
from tests.order.conftest import order_data


class TestAllocation:
    @pytest.mark.parametrize(
        argnames='difference,response',
        argvalues=(
            pytest.param(-1, True, id='purchased_quantity > ordered_quantity'),
            pytest.param(1, False, id='purchased_quantity < ordered_quantity'),
            pytest.param(0, True, id='purchased_quantity == ordered_quantity'),
        ),
    )
    def test__can_allocate__check_quantity(
        self,
        difference: int,
        response: bool,
    ):
        BatchData = batch_data()
        ordered_quantity = BatchData.purchased_quantity + difference
        OrderData = order_data(ordered_quantity=ordered_quantity)

        batch = Batch(**BatchData.asdict())
        order = OrderLine(**OrderData.asdict())

        assert batch.can_allocate(order) is response

    @pytest.mark.parametrize(
        argnames='can_allocate',
        argvalues=(
            pytest.param(True, id='batch.product_name == order.product_name'),
            pytest.param(False, id='batch.product_name != order.product_name'),
        ),
    )
    def test__can_allocate__check_product_name(self, can_allocate: bool):
        BatchData = batch_data()
        order_name = BatchData.product_name
        if can_allocate is False:
            order_name = f'{order_name} (NEW)'
        OrderData = order_data(product_name=order_name)

        batch = Batch(**BatchData.asdict())
        order = OrderLine(**OrderData.asdict())

        assert batch.can_allocate(order) is can_allocate

    def test_quantity_after_allocation(self):
        BatchData = batch_data()
        OrderData = order_data()

        batch = Batch(**BatchData.asdict())
        order = OrderLine(**OrderData.asdict())
        batch.allocate(order)

        assert batch.purchased_quantity == BatchData.purchased_quantity
        assert batch.allocations == [order]
        assert batch.allocated_quantity == OrderData.ordered_quantity
        assert batch.available_quantity == (
            BatchData.purchased_quantity - OrderData.ordered_quantity
        )

    def test_order_quantity_great_than_purchased_quantity(self):
        BatchData = batch_data()
        ordered_quantity = BatchData.purchased_quantity + 1
        OrderData = order_data(ordered_quantity=ordered_quantity)

        batch = Batch(**BatchData.asdict())
        order = OrderLine(**OrderData.asdict())
        batch.allocate(order)

        assert batch.purchased_quantity == BatchData.purchased_quantity
        assert batch.allocations == list()
        assert batch.allocated_quantity == 0
        assert batch.available_quantity == BatchData.purchased_quantity

    def test_order_with_differ_product_name(self):
        BatchData = batch_data()
        product_name = f'{BatchData.product_name} (NEW)'
        OrderData = order_data(product_name=product_name)

        batch = Batch(**BatchData.asdict())
        order = OrderLine(**OrderData.asdict())
        batch.allocate(order)

        assert batch.purchased_quantity == BatchData.purchased_quantity
        assert batch.available_quantity == BatchData.purchased_quantity
        assert batch.allocated_quantity == 0
        assert batch.allocations == list()

    def test_if_add_already_allocated_order_this_substitute_oldest(self):
        BatchData = batch_data()
        OrderDataOld = order_data(ordered_quantity=2)
        OrderDataNew = order_data(id=OrderDataOld.id, ordered_quantity=4)

        batch = Batch(**BatchData.asdict())
        order_old = OrderLine(**OrderDataOld.asdict())
        order_new = OrderLine(**OrderDataNew.asdict())

        batch.allocate(order_old)
        batch.allocate(order_new)

        assert batch.allocations == [order_new]
        assert batch.allocated_quantity == order_new.ordered_quantity
        assert batch.available_quantity == (
            batch.purchased_quantity - order_new.ordered_quantity
        )


class TestDeallocation:
    def test_allocated(self):
        BatchData = batch_data()
        OrderData = order_data()

        batch = Batch(**BatchData.asdict())
        order = OrderLine(**OrderData.asdict())

        batch.allocate(order)
        assert batch.purchased_quantity == BatchData.purchased_quantity
        assert batch.available_quantity == (
            BatchData.purchased_quantity - OrderData.ordered_quantity
        )
        assert batch.allocated_quantity == OrderData.ordered_quantity
        assert batch.allocations == [order]

        batch.deallocate(order)
        assert batch.purchased_quantity == BatchData.purchased_quantity
        assert batch.available_quantity == BatchData.purchased_quantity
        assert batch.allocated_quantity == 0
        assert batch.allocations == list()

    def test_not_allocated(self):
        BatchData = batch_data()
        OrderData = order_data()

        batch = Batch(**BatchData.asdict())
        order = OrderLine(**OrderData.asdict())
        assert batch.allocations == list()

        batch.deallocate(order)
        assert batch.purchased_quantity == BatchData.purchased_quantity
        assert batch.available_quantity == BatchData.purchased_quantity
        assert batch.allocated_quantity == 0
        assert batch.allocations == list()
