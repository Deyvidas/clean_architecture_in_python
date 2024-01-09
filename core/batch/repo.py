from dataclasses import dataclass
from typing import Any

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.base.repo import AbstractSqlAlchemyRepo
from core.batch.models import Batch
from core.batch.orm import BatchOrm


@dataclass
class BatchRepoSqlAlchemy(AbstractSqlAlchemyRepo):
    session: Session

    def add(self, model: Batch) -> Batch:
        orm = self.model_to_orm(model)
        self.session.add(orm)
        self.session.commit()
        model = self.orm_to_model(orm)
        return model

    def get(self, **filters: Any) -> list[Batch]:
        stmt = select(BatchOrm).filter_by(**filters)
        orms = self.session.scalars(stmt).unique().all()
        models = [self.orm_to_model(o) for o in orms]
        return models

    def model_to_orm(self, model: Batch) -> BatchOrm:
        kwargs = TypeAdapter(Batch).dump_python(model)
        return BatchOrm(**kwargs)

    def orm_to_model(self, orm: BatchOrm) -> Batch:
        return TypeAdapter(Batch).validate_python(orm)
