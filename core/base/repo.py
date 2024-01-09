from abc import ABC
from abc import abstractmethod
from typing import Any

from core.base.models import MyBaseModel


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, model: MyBaseModel) -> MyBaseModel:
        raise NotImplementedError

    @abstractmethod
    def get(self, **filters: Any) -> MyBaseModel:
        raise NotImplementedError
