from datetime import date
from typing import NotRequired
from typing import Unpack
from typing import override

from sqlalchemy import select

from core.base.repo import AbstractSqlAlchemyRepo
from core.base.repo import Filters
from core.batch.models import Batch
from core.batch.orm import BatchOrm
from core.order.repo import OrderLineRepoSqlAlchemy


class BatchFilters(Filters):
    product_name: NotRequired[str]
    purchased_quantity: NotRequired[int]
    estimated_arrival_date: NotRequired[date]


class BatchRepoSqlAlchemy(AbstractSqlAlchemyRepo[Batch, BatchOrm]):
    model = Batch
    orm = BatchOrm

    @override
    def add(self, model: Batch) -> Batch:
        orm = self.model_to_orm(model)
        self.session.add(orm)
        model = self.orm_to_model(orm)
        return model

    @override
    def get(self, **filters: Unpack[BatchFilters]) -> list[Batch]:
        stmt = select(self.orm).filter_by(**filters)
        orms = self.session.scalars(stmt).unique().all()
        models = self.orms_to_models(list(orms))
        return models

    @override
    def model_to_orm(self, model: Batch) -> BatchOrm:
        kw = self.single_adapter.dump_python(model, exclude={'allocations'})
        order_repo = OrderLineRepoSqlAlchemy(self.session)
        return self.orm(
            allocations=order_repo.models_to_orms(model.allocations),
            **kw,
        )

    @override
    def orm_to_model(self, orm: BatchOrm) -> Batch:
        model = super().orm_to_model(orm)
        order_repo = OrderLineRepoSqlAlchemy(self.session)
        for order_orm in orm.allocations:
            model.allocate(order_repo.orm_to_model(order_orm))
        return model
