from functools import wraps
from typing import Any
from typing import Callable
from typing import Literal
from typing import Self
from typing import TypeAlias

import pytest
from pydantic import BaseModel
from pydantic import TypeAdapter
from pydantic_core import ErrorDetails

from config.sqlalchemy_config import engine_config
from config.sqlalchemy_config import session_config
from core.base.orm import BaseOrm
from tests.batch.conftest import batch_factory
from tests.order.conftest import order_factory


__all__ = [
    'batch_factory',
    'order_factory',
]


@pytest.fixture
def tables():
    metadata = BaseOrm.metadata
    engine = engine_config.engine
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture
def session():
    with session_config.session() as s:
        yield s


class ErrorDetailsModel(BaseModel):
    """Model that represents details of a Pydantic validation error."""

    loc: tuple[int | str, ...]
    type: str
    ctx: dict[str, Any] | None = None
    msg: str
    input: Any

    @classmethod
    def make(cls, errors: list[ErrorDetails]) -> list[Self]:
        return TypeAdapter(list[cls]).validate_python(errors)  # type: ignore[valid-type]


Scope: TypeAlias = Literal[
    'function',
    'class',
    'module',
    'package',
    'session',
]


def dependency(depends: list[str] = list(), scope: Scope = 'session'):
    def get_func(func: Callable):
        @wraps(func)
        @pytest.mark.dependency(depends=depends, scope=scope)
        @pytest.mark.order(after=depends)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return get_func
