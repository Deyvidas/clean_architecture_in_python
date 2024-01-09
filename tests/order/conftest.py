from __future__ import annotations

from dataclasses import dataclass

from core.utils.default_factories import get_hex_uuid4
from tests.batch.conftest import batch_data
from tests.utils import BaseData


def order_data(**kwargs) -> OrderData:
    return OrderData(
        id=kwargs.get('id', get_hex_uuid4()),
        product_name=kwargs.get('product_name', batch_data().product_name),
        ordered_quantity=kwargs.get('ordered_quantity', 2),
    )


@dataclass(frozen=True, kw_only=True)
class OrderData(BaseData):
    id: str
    product_name: str
    ordered_quantity: int
