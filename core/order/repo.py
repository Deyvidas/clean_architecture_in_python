from typing import NotRequired
from typing import Unpack
from typing import override

from sqlalchemy import select

from core.base.repo import AbstractSqlAlchemyRepo
from core.base.repo import Filters
from core.order.models import OrderLine
from core.order.orm import OrderLineOrm


class OrderLineFilters(Filters):
    product_name: NotRequired[str]
    ordered_quantity: NotRequired[int]


class OrderLineRepoSqlAlchemy(AbstractSqlAlchemyRepo[OrderLine, OrderLineOrm]):
    model = OrderLine
    orm = OrderLineOrm

    @override
    def add(self, model: OrderLine) -> OrderLine:
        orm = self.model_to_orm(model)
        self.session.add(orm)
        model = self.orm_to_model(orm)
        return model

    @override
    def get(self, **filters: Unpack[Filters]) -> list[OrderLine]:
        stmt = select(OrderLineOrm).filter_by(**filters)
        orms = self.session.scalars(stmt).unique().all()
        models = [self.orm_to_model(o) for o in orms]
        return models
