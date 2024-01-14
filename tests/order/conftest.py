from __future__ import annotations

import pytest

from tests.factories.order import OrderLineFactory


@pytest.fixture
def order_factory() -> OrderLineFactory:
    return OrderLineFactory()
