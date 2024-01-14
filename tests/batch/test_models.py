import pytest

from tests.factories.batch import BatchFactory
from tests.factories.order import OrderLineFactory


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
        batch_factory: BatchFactory,
        order_factory: OrderLineFactory,
    ):
        batch = batch_factory.generate_one()
        purchased_quantity = batch.purchased_quantity
        order = order_factory.generate_one(
            product_name=batch.product_name,
            ordered_quantity=purchased_quantity + difference,
        )

        assert batch.can_allocate(order) is response

    @pytest.mark.parametrize(
        argnames='can_allocate',
        argvalues=(
            pytest.param(True, id='batch.product_name == order.product_name'),
            pytest.param(False, id='batch.product_name != order.product_name'),
        ),
    )
    def test__can_allocate__check_product_name(
        self,
        can_allocate: bool,
        batch_factory: BatchFactory,
        order_factory: OrderLineFactory,
    ):
        batch = batch_factory.generate_one()
        product_name = batch.product_name
        if can_allocate is False:
            product_name = f'{product_name} (NEW)'
        order = order_factory.generate_one(product_name=product_name)

        assert batch.can_allocate(order) is can_allocate

    def test_quantity_after_allocation(
        self,
        batch_factory: BatchFactory,
        order_factory: OrderLineFactory,
    ):
        batch = batch_factory.generate_one()
        order = order_factory.generate_one(product_name=batch.product_name)
        batch.allocate(order)

        assert batch.allocations == [order]
        assert batch.allocated_quantity == order.ordered_quantity
        assert batch.available_quantity == (
            batch.purchased_quantity - order.ordered_quantity
        )

    def test_order_quantity_great_than_purchased_quantity(
        self,
        batch_factory: BatchFactory,
        order_factory: OrderLineFactory,
    ):
        batch = batch_factory.generate_one()
        order = order_factory.generate_one(
            product_name=batch.product_name,
            ordered_quantity=batch.purchased_quantity + 1,
        )
        batch.allocate(order)

        assert batch.allocations == list()
        assert batch.allocated_quantity == 0
        assert batch.available_quantity == batch.purchased_quantity

    def test_order_with_differ_product_name(
        self,
        batch_factory: BatchFactory,
        order_factory: OrderLineFactory,
    ):
        batch = batch_factory.generate_one()
        order = order_factory.generate_one()
        batch.allocate(order)

        assert batch.allocated_quantity == 0
        assert batch.allocations == list()
        assert batch.available_quantity == batch.purchased_quantity

    def test_if_add_already_allocated_order_this_substitute_oldest(
        self,
        batch_factory: BatchFactory,
        order_factory: OrderLineFactory,
    ):
        batch = batch_factory.generate_one()
        order_old = order_factory.generate_one(
            product_name=batch.product_name,
        )
        order_new = order_factory.generate_one(
            product_name=batch.product_name,
            id=order_old.id,
        )

        batch.allocate(order_old)
        batch.allocate(order_new)

        assert batch.allocations == [order_new]
        assert batch.allocated_quantity == order_new.ordered_quantity
        assert batch.available_quantity == (
            batch.purchased_quantity - order_new.ordered_quantity
        )


class TestDeallocation:
    def test_allocated(
        self,
        batch_factory: BatchFactory,
        order_factory: OrderLineFactory,
    ):
        batch = batch_factory.generate_one()
        order = order_factory.generate_one(product_name=batch.product_name)

        batch.allocate(order)
        batch.deallocate(order)
        assert batch.available_quantity == batch.purchased_quantity
        assert batch.allocated_quantity == 0
        assert batch.allocations == list()

    def test_not_allocated(
        self,
        batch_factory: BatchFactory,
        order_factory: OrderLineFactory,
    ):
        batch = batch_factory.generate_one()
        order = order_factory.generate_one(product_name=batch.product_name)
        assert batch.allocations == list()

        batch.deallocate(order)
        assert batch.available_quantity == batch.purchased_quantity
        assert batch.allocated_quantity == 0
        assert batch.allocations == list()
