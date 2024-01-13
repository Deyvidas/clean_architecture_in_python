from random import randint

from polyfactory import Use

from core.order.models import OrderLine
from core.utils.default_factories import get_hex_uuid4
from tests.factories.base import BaseFactory


class OrderLineFactory(BaseFactory[OrderLine]):
    __model__ = OrderLine

    id = Use(get_hex_uuid4)
    ordered_quantity = Use(lambda: randint(10**2, 10**3))
