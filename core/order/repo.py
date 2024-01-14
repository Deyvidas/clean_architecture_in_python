from typing import NotRequired
from typing import Unpack
from typing import override

from core.base.repo import BaseSqlAlchemyRepo
from core.base.repo import Filters
from core.order.models import OrderLine
from core.order.orm import OrderLineOrm


class OrderLineFilters(Filters):
    product_name: NotRequired[str]
    ordered_quantity: NotRequired[int]


class OrderLineRepoSqlAlchemy(BaseSqlAlchemyRepo[OrderLine, OrderLineOrm]):
    model = OrderLine
    orm = OrderLineOrm

    @override
    def get(self, **filters: Unpack[OrderLineFilters]) -> list[OrderLine]:
        return super().get(**filters)  # type: ignore[misc]
