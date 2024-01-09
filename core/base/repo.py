from abc import ABC
from abc import abstractmethod
from typing import Any

from core.base.models import MyBaseModel
from core.base.orm import BaseOrm


class AbstractRepo(ABC):
    """Interface for interacting with data storage."""

    @abstractmethod
    def add(self, model: MyBaseModel) -> MyBaseModel:
        raise NotImplementedError

    @abstractmethod
    def get(self, **filters: Any) -> list[MyBaseModel]:
        raise NotImplementedError


class AbstractSqlAlchemyRepo(AbstractRepo):
    """Interface for interacting with db using SQLAlchemy framework."""

    @abstractmethod
    def model_to_orm(self, model: MyBaseModel) -> BaseOrm:
        raise NotImplementedError

    @abstractmethod
    def orm_to_model(self, orm: BaseOrm) -> MyBaseModel:
        raise NotImplementedError
