from datetime import date
from typing import Any

import pytest

from batch.models import Batch
from order.models import OrderLine
from utils.utils_for_tests import update_data


def batch_data(**kwargs) -> dict[str, Any]:
    data = {
        'id': 'ed61488f1ed84a58928bd2baeaf72bd0',
        'product_name': 'SMALL-TABLE',
        'purchased_quantity': 20,
        'estimated_arrival_date': date.today(),
    }
    return update_data(data, kwargs)


def order_data(**kwargs) -> dict[str, Any]:
    data = {
        'id': 'bb8555066c5d4fef96dbbbad0aac3a4a',
        'product_name': 'SMALL-TABLE',
        'ordered_quantity': 2,
    }
    return update_data(data, kwargs)


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
        _batch_data = batch_data()
        purchased_quantity = _batch_data['purchased_quantity']
        ordered_quantity = purchased_quantity + difference

        batch = Batch(**_batch_data)
        order = OrderLine(**order_data(ordered_quantity=ordered_quantity))

        assert batch.can_allocate(order) is response

    @pytest.mark.parametrize(
        argnames='can_allocate',
        argvalues=(
            pytest.param(True, id='batch.product_name == order.product_name'),
            pytest.param(False, id='batch.product_name != order.product_name'),
        ),
    )
    def test__can_allocate__check_product_name(self, can_allocate: bool):
        _batch_data = batch_data()
        batch_name = _batch_data['product_name']
        order_name = batch_name if can_allocate else f'{batch_name} (NEW)'

        batch = Batch(**_batch_data)
        order = OrderLine(**order_data(product_name=order_name))

        assert batch.can_allocate(order) is can_allocate

    def test_quantity_after_allocation(self):
        _batch_data = batch_data()
        _order_data = order_data()
        batch_quantity = _batch_data['purchased_quantity']
        order_quantity = _order_data['ordered_quantity']

        batch = Batch(**_batch_data)
        order = OrderLine(**_order_data)
        batch.allocate(order)

        assert batch.purchased_quantity == batch_quantity
        assert batch.allocations == set([order])
        assert batch.allocated_quantity == order_quantity
        assert batch.available_quantity == batch_quantity - order_quantity

    def test_order_quantity_great_than_purchased_quantity(self):
        _batch_data = batch_data()
        batch_quantity = _batch_data['purchased_quantity']

        batch = Batch(**_batch_data)
        order = OrderLine(**order_data(ordered_quantity=batch_quantity + 1))
        batch.allocate(order)

        assert batch.purchased_quantity == batch_quantity
        assert batch.allocations == set()
        assert batch.allocated_quantity == 0
        assert batch.available_quantity == batch_quantity

    def test_order_with_differ_product_name(self):
        _batch_data = batch_data()
        batch_quantity = _batch_data['purchased_quantity']
        batch_name = _batch_data['product_name']

        batch = Batch(**_batch_data)
        order = OrderLine(**order_data(product_name=f'{batch_name} (NEW)'))
        batch.allocate(order)

        assert batch.purchased_quantity == batch_quantity
        assert batch.available_quantity == batch_quantity
        assert batch.allocated_quantity == 0
        assert batch.allocations == set()


class TestDeallocation:
    def test_allocated(self):
        _batch_data = batch_data()
        _order_data = order_data()
        batch_quantity = _batch_data['purchased_quantity']
        order_quantity = _order_data['ordered_quantity']

        batch = Batch(**_batch_data)
        order = OrderLine(**_order_data)

        batch.allocate(order)
        assert batch.purchased_quantity == batch_quantity
        assert batch.available_quantity == batch_quantity - order_quantity
        assert batch.allocated_quantity == order_quantity
        assert batch.allocations == set([order])

        batch.deallocate(order)
        assert batch.purchased_quantity == batch_quantity
        assert batch.available_quantity == batch_quantity
        assert batch.allocated_quantity == 0
        assert batch.allocations == set()
