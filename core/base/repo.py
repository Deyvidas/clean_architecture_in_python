from abc import ABC
from abc import abstractmethod
from typing import NotRequired
from typing import TypedDict
from typing import Unpack

from pydantic import TypeAdapter
from sqlalchemy.orm.session import Session

from core.base.models import MyBaseModel
from core.base.orm import BaseOrm


class Filters(TypedDict):
    id: NotRequired[str]


class AbstractRepo(ABC):
    """Interface for interacting with data storage."""

    @abstractmethod
    def add(self, model: MyBaseModel) -> MyBaseModel:
        raise NotImplementedError

    @abstractmethod
    def get(self, **filters: Unpack[Filters]) -> list[MyBaseModel]:
        raise NotImplementedError


class AbstractSqlAlchemyRepo(AbstractRepo):
    """Interface for interacting with db using SQLAlchemy framework."""

    def __init__(
        self,
        session: Session,
        model: type[MyBaseModel],
        orm: type[BaseOrm],
    ):
        self.session = session
        self.model = model
        self.orm = orm

        self.sing_adapter = TypeAdapter(model)
        self.many_adapter = TypeAdapter(list[model])  # type: ignore[valid-type]

    def model_to_orm(self, model: MyBaseModel) -> BaseOrm:
        return self.orm(**self.sing_adapter.dump_python(model))

    def orm_to_model(self, orm: BaseOrm) -> MyBaseModel:
        return self.sing_adapter.validate_python(orm)

    def models_to_orms(self, models: list[MyBaseModel]) -> list[BaseOrm]:
        return [self.model_to_orm(m) for m in models]

    def orms_to_models(self, orms: list[BaseOrm]) -> list[MyBaseModel]:
        return [self.orm_to_model(o) for o in orms]
