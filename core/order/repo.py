from dataclasses import dataclass
from typing import Any

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.base.repo import AbstractSqlAlchemyRepo
from core.order.models import OrderLine
from core.order.orm import OrderLineOrm


@dataclass
class OrderLineRepoSqlAlchemy(AbstractSqlAlchemyRepo):
    session: Session

    def add(self, model: OrderLine) -> OrderLine:
        orm = self.model_to_orm(model)
        self.session.add(orm)
        self.session.commit()
        model = self.orm_to_model(orm)
        return model

    def get(self, **filters: Any) -> list[OrderLine]:
        stmt = select(OrderLineOrm).filter_by(**filters)
        orms = self.session.scalars(stmt).unique().all()
        models = [self.orm_to_model(o) for o in orms]
        return models

    def model_to_orm(self, model: OrderLine) -> OrderLineOrm:
        kwargs = TypeAdapter(OrderLine).dump_python(model)
        return OrderLineOrm(**kwargs)

    def orm_to_model(self, orm: OrderLineOrm) -> OrderLine:
        return TypeAdapter(OrderLine).validate_python(orm)
