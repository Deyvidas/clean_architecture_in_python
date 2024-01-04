from datetime import date
from typing import Any

import pytest

from batch.models import Batch
from order.models import OrderLine
from utils.utils_for_tests import update_data


def batch_data(**kwargs) -> dict[str, Any]:
    data = {
        'reference': 'batch-001',
        'product_name': 'SMALL-TABLE',
        'purchased_quantity': 20,
        'estimated_arrival_date': date.today(),
    }
    return update_data(data, kwargs)


def order_data(**kwargs) -> dict[str, Any]:
    data = {
        'id': 1,
        'product_name': 'SMALL-TABLE',
        'ordered_quantity': 2,
    }
    return update_data(data, kwargs)


class TestAllocation:

    def test_available_quantity_is_reduced_after_allocation(self):
        batch = Batch(**batch_data())
        order = OrderLine(**order_data())

        batch.allocate(order)

        assert batch.purchased_quantity == 20
        assert batch.available_quantity == 18
        assert batch.allocated_quantity == 2

    @pytest.mark.parametrize(
        argnames='purchased,ordered,response',
        argvalues=(
            pytest.param(
                20, 2, True, id='purchased_quantity > ordered_quantity'
            ),
            pytest.param(
                2, 20, False, id='purchased_quantity < ordered_quantity'
            ),
            pytest.param(
                2, 2, True, id='purchased_quantity == ordered_quantity'
            ),
        ),
    )
    def test__can_allocate__check_quantity(
        self,
        purchased: int,
        ordered: int,
        response: bool,
    ):
        batch = Batch(**batch_data(purchased_quantity=purchased))
        order = OrderLine(**order_data(ordered_quantity=ordered))

        assert batch.can_allocate(order) is response

    @pytest.mark.parametrize(
        argnames='batch_name,order_name,response',
        argvalues=(
            pytest.param(
                'SMALL-TABLE',
                'SMALL-TABLE',
                True,
                id='batch.product_name == order.product_name',
            ),
            pytest.param(
                'SMALL-TABLE',
                'BEDSIDE-TABLE',
                False,
                id='batch.product_name != order.product_name',
            ),
        ),
    )
    def test__can_allocate__check_product_name(
        self,
        batch_name: str,
        order_name: str,
        response: bool,
    ):
        batch = Batch(**batch_data(product_name=batch_name))
        order = OrderLine(**order_data(product_name=order_name))

        assert batch.can_allocate(order) is response


def test__deallocate__can_deallocate_only_allocated():
    ...
