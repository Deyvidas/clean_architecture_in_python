from __future__ import annotations

from dataclasses import dataclass

from core.utils.default_factories import get_hex_uuid4
from tests.utils import BaseData
from tests.utils import update_data


def order_data(**kwargs) -> OrderData:
    data = {
        'id': get_hex_uuid4(),
        'product_name': 'SMALL-TABLE',
        'ordered_quantity': 2,
    }
    data = update_data(data, kwargs)
    return OrderData(**data)


@dataclass(frozen=True, kw_only=True)
class OrderData(BaseData):
    id: str
    product_name: str
    ordered_quantity: int
