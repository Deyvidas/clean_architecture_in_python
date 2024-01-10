from datetime import date
from typing import NotRequired
from typing import Unpack
from typing import override

from sqlalchemy import select

from core.base.models import MyBaseModel
from core.base.orm import BaseOrm
from core.base.repo import AbstractSqlAlchemyRepo
from core.base.repo import Filters
from core.batch.models import Batch
from core.batch.orm import BatchOrm
from core.order.models import OrderLine
from core.order.orm import OrderLineOrm
from core.order.repo import OrderLineRepoSqlAlchemy


class BatchFilters(Filters):
    product_name: NotRequired[str]
    purchased_quantity: NotRequired[int]
    estimated_arrival_date: NotRequired[date]


class BatchRepoSqlAlchemy(AbstractSqlAlchemyRepo):
    @override
    def add(self, model: MyBaseModel) -> MyBaseModel:
        orm = self.model_to_orm(model)
        self.session.add(orm)
        model = self.orm_to_model(orm)
        return model

    @override
    def get(self, **filters: Unpack[BatchFilters]) -> list[MyBaseModel]:
        stmt = select(BatchOrm).filter_by(**filters)
        orms = self.session.scalars(stmt).unique().all()
        models = self.orms_to_models(list(orms))
        return models

    @override
    def model_to_orm(self, model: MyBaseModel) -> BaseOrm:
        kwargs = self.sing_adapter.dump_python(model)
        orders_kwargs = kwargs.pop('allocations', list())
        kwargs['allocations'] = list()

        o_r = OrderLineRepoSqlAlchemy(self.session, OrderLine, OrderLineOrm)
        for kw in orders_kwargs:
            order = o_r.orm(batch_id=model.id, **kw)
            kwargs['allocations'].append(order)

        return self.orm(**kwargs)

    @override
    def orm_to_model(self, orm: BaseOrm) -> MyBaseModel:
        if not isinstance(orm, BatchOrm):
            raise TypeError

        model = super().orm_to_model(orm)
        if not isinstance(model, Batch):
            raise TypeError

        o_r = OrderLineRepoSqlAlchemy(self.session, OrderLine, OrderLineOrm)
        for order_orm in orm.allocations:
            order = o_r.orm_to_model(order_orm)
            if not isinstance(order, OrderLine):
                raise TypeError
            model.allocate(order)

        return model
