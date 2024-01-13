from typing import Generic

from polyfactory.factories.pydantic_factory import ModelFactory

from core.base.repo import BM


class BaseFactory(ModelFactory, Generic[BM]):
    __is_base_factory__ = True

    @classmethod
    def generate_one(cls) -> BM:
        return cls.build(factory_use_construct=True)

    @classmethod
    def generate_many(cls, qnt: int) -> list[BM]:
        return cls.batch(size=qnt, factory_use_construct=True)
