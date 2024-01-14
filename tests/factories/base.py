from typing import Any
from typing import Callable
from typing import Generic

from polyfactory.factories.pydantic_factory import ModelFactory

from core.base.repo import BM


def check_kwargs(function: Callable):
    def wrap(*args, **kwargs):
        model_fields = args[0].__model__.model_fields
        extra = set(kwargs) - set(model_fields)
        if extra == set():
            return function(*args, **kwargs)
        raise AttributeError(f'Passed extra attributes [{', '.join(extra)}].')

    return wrap


class BaseFactory(ModelFactory, Generic[BM]):
    __is_base_factory__ = True

    @classmethod
    @check_kwargs
    def generate_one(cls, **kwargs: Any) -> BM:
        return cls.build(factory_use_construct=True, **kwargs)

    @classmethod
    @check_kwargs
    def generate_many(cls, qnt: int, **kwargs: Any) -> list[BM]:
        return cls.batch(size=qnt, factory_use_construct=True, **kwargs)
