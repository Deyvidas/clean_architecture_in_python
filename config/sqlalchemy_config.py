from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config_dict
from config.postgresql_config import postgresql_config


class EngineConfig(BaseModel):
    url: str
    echo: bool | None = Field(default=True)
    pool_size: int | None = Field(default=5)
    max_overflow: int | None = Field(default=10)
    connect_args: dict[str, Any] | None = Field(default_factory=dict)

    @property
    def engine(self) -> Engine:
        return create_engine(**vars(self))


engine_conf_dict = config_dict.get('sqla_engine_settings', dict())
db_url = postgresql_config.url
engine_config = EngineConfig(url=db_url, **engine_conf_dict)


class SessionConfig(BaseModel):
    bind: Engine
    autoflush: bool | None = Field(default=True)
    expire_on_commit: bool | None = Field(default=False)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @property
    def session(self):
        return sessionmaker(**vars(self))


session_conf_dict = config_dict.get('sqla_engine_settings', dict())
session_config = SessionConfig(bind=engine_config.engine, **session_conf_dict)
