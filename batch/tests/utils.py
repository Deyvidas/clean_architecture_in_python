from __future__ import annotations

import uuid

from dataclasses import dataclass
from datetime import date

from utils.utils_for_tests import BaseData
from utils.utils_for_tests import update_data


def batch_data(**kwargs) -> BatchData:
    data = {
        'id': uuid.uuid4().hex,
        'product_name': 'SMALL-TABLE',
        'purchased_quantity': 20,
        'estimated_arrival_date': date.today(),
    }
    data = update_data(data, kwargs)
    return BatchData(**data)


def order_data(**kwargs) -> OrderData:
    data = {
        'id': uuid.uuid4().hex,
        'product_name': 'SMALL-TABLE',
        'ordered_quantity': 2,
    }
    data = update_data(data, kwargs)
    return OrderData(**data)


@dataclass(frozen=True, kw_only=True)
class BatchData(BaseData):
    id: str
    product_name: str
    purchased_quantity: int
    estimated_arrival_date: date


@dataclass(frozen=True, kw_only=True)
class OrderData(BaseData):
    id: str
    product_name: str
    ordered_quantity: int
