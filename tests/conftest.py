import pytest

from config.sqlalchemy_config import engine_config
from config.sqlalchemy_config import session_config
from core.base.orm import BaseOrm


@pytest.fixture(autouse=True)
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
