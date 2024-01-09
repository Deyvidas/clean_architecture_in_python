from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from core.utils.default_factories import get_hex_uuid4
from tests.utils import BaseData
from tests.utils import update_data


def batch_data(**kwargs) -> BatchData:
    data = {
        'id': get_hex_uuid4(),
        'product_name': 'SMALL-TABLE',
        'purchased_quantity': 20,
        'estimated_arrival_date': date.today(),
    }
    data = update_data(data, kwargs)
    return BatchData(**data)


@dataclass(frozen=True, kw_only=True)
class BatchData(BaseData):
    id: str
    product_name: str
    purchased_quantity: int
    estimated_arrival_date: date
