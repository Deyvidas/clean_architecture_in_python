from dataclasses import dataclass
from typing import Any
from typing import override

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.base.models import MyBaseModel
from core.base.orm import BaseOrm
from core.base.repo import AbstractSqlAlchemyRepo
from core.batch.models import Batch
from core.batch.orm import BatchOrm
from core.order.models import OrderLine
from core.order.repo import OrderLineRepoSqlAlchemy


@dataclass
class BatchRepoSqlAlchemy(AbstractSqlAlchemyRepo):
    session: Session

    @override
    def add(self, model: MyBaseModel) -> MyBaseModel:
        orm = self.model_to_orm(model)
        self.session.add(orm)
        self.session.commit()
        model = self.orm_to_model(orm)
        return model

    @override
    def get(self, **filters: Any) -> list[MyBaseModel]:
        stmt = select(BatchOrm).filter_by(**filters)
        orms = self.session.scalars(stmt).unique().all()
        models = [self.orm_to_model(o) for o in orms]
        return models

    @override
    def model_to_orm(self, model: MyBaseModel) -> BaseOrm:
        if not isinstance(model, Batch):
            raise TypeError

        kwargs = model.model_dump()
        order_repo = OrderLineRepoSqlAlchemy(self.session)
        kwargs['_allocations'] = set(
            order_repo.model_to_orm(o) for o in model.allocations
        )

        orm = BatchOrm(**kwargs)
        return orm

    @override
    def orm_to_model(self, orm: BaseOrm) -> MyBaseModel:
        if not isinstance(orm, BatchOrm):
            raise TypeError

        model = TypeAdapter(Batch).validate_python(orm)

        order_repo = OrderLineRepoSqlAlchemy(self.session)
        for order_orm in orm._allocations:
            order_model = order_repo.orm_to_model(order_orm)
            if not isinstance(order_model, OrderLine):
                raise TypeError
            model.allocate(order_model)
        return model
