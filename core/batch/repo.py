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
        kwargs = TypeAdapter(Batch).dump_python(model)
        return BatchOrm(**kwargs)

    @override
    def orm_to_model(self, orm: BaseOrm) -> MyBaseModel:
        return TypeAdapter(Batch).validate_python(orm)
