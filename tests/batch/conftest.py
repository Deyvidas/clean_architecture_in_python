from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import NotRequired
from typing import TypedDict
from typing import Unpack

from core.utils.default_factories import get_hex_uuid4
from tests.utils import BaseData


class BatchDataKwargs(TypedDict):
    id: NotRequired[str]
    product_name: NotRequired[str]
    purchased_quantity: NotRequired[int]
    estimated_arrival_date: NotRequired[date | None]


def batch_data(**kwargs: Unpack[BatchDataKwargs]) -> BatchData:
    return BatchData(
        id=kwargs.get('id', get_hex_uuid4()),
        product_name=kwargs.get('product_name', 'SMALL-TABLE'),
        purchased_quantity=kwargs.get('purchased_quantity', 20),
        estimated_arrival_date=kwargs.get(
            'estimated_arrival_date',
            date.today(),
        ),
    )


@dataclass(frozen=True, kw_only=True)
class BatchData(BaseData):
    id: str
    product_name: str
    purchased_quantity: int
    estimated_arrival_date: date | None
