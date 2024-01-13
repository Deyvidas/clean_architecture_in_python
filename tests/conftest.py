from functools import wraps
from typing import Callable
from typing import Literal
from typing import TypeAlias

import pytest

from config.sqlalchemy_config import engine_config
from config.sqlalchemy_config import session_config
from core.base.orm import BaseOrm


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
