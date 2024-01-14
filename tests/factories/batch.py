from random import randint

from polyfactory import Use

from core.batch.models import Batch
from core.utils.default_factories import get_hex_uuid4
from tests.factories.base import BaseFactory


class BatchFactory(BaseFactory[Batch]):
    __model__ = Batch

    id = Use(get_hex_uuid4)
    ordered_quantity = Use(lambda: randint(10**4, 10**5))
