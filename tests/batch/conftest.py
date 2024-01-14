from __future__ import annotations

import pytest

from tests.factories.batch import BatchFactory


@pytest.fixture
def batch_factory() -> BatchFactory:
    return BatchFactory()
