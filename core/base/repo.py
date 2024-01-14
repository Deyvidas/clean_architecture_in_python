from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import NotRequired
from typing import TypedDict
from typing import TypeVar
from typing import Unpack
from typing import override

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.base.models import MyBaseModel
from core.base.orm import BaseOrm


class Filters(TypedDict):
    id: NotRequired[str]


BM = TypeVar('BM', bound=MyBaseModel)
OM = TypeVar('OM', bound=BaseOrm)


class AbstractRepo(ABC, Generic[BM]):
    """Interface for interacting with data storage."""

    @abstractmethod
    def add(self, model: BM) -> BM:
        raise NotImplementedError

    @abstractmethod
    def get(self, **filters: Unpack[Filters]) -> list[BM]:
        raise NotImplementedError


class BaseSqlAlchemyRepo(AbstractRepo[BM], Generic[BM, OM]):
    """Interface for interacting with db using SQLAlchemy framework."""

    model: type[BM]
    orm: type[OM]

    def __init__(self, session: Session):
        self.session = session

    @override
    def add(self, model: BM) -> BM:
        orm = self.model_to_orm(model)
        self.session.add(orm)
        model = self.orm_to_model(orm)
        return model

    @override
    def get(self, **filters: Unpack[Filters]) -> list[BM]:
        stmt = select(self.orm).filter_by(**filters)
        orms = self.session.scalars(stmt).unique().all()
        models = self.orms_to_models(list(orms))
        return models

    @property
    def single_adapter(self) -> TypeAdapter[BM]:
        return TypeAdapter(self.model)

    @property
    def many_adapter(self) -> TypeAdapter[list[BM]]:
        return TypeAdapter(list[self.model])  # type: ignore[name-defined]

    def model_to_orm(self, model: BM) -> OM:
        return self.orm(**self.single_adapter.dump_python(model))

    def orm_to_model(self, orm: OM) -> BM:
        return self.single_adapter.validate_python(orm)

    def models_to_orms(self, models: list[BM]) -> list[OM]:
        return [self.model_to_orm(m) for m in models]

    def orms_to_models(self, orms: list[OM]) -> list[BM]:
        return [self.orm_to_model(o) for o in orms]
