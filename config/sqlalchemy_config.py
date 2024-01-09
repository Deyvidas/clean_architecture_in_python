from typing import Any

from pydantic import Field
from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

from config import config_dict
from config.base_config import BaseConfig
from config.postgresql_config import postgresql_config


class EngineConfig(BaseConfig):
    url: str
    echo: bool | None = Field(default=True)
    pool_size: int | None = Field(default=5)
    max_overflow: int | None = Field(default=10)
    create_db: bool | None = Field(default=False)
    connect_args: dict[str, Any] | None = Field(default_factory=dict)

    @property
    def engine(self) -> Engine:
        if self.create_db is True:
            self._create_db_if_not_exists()

        return create_engine(
            url=self.url,
            echo=self.echo,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            connect_args=self.connect_args,
        )

    def _create_db_if_not_exists(self):
        """Check if the db with the url exists and create if not, else pass."""
        if not database_exists(self.url):
            create_database(self.url)


engine_conf_dict = config_dict.get('sqla_engine_settings', dict())
db_url = postgresql_config.url
engine_config = EngineConfig(url=db_url, **engine_conf_dict)


class SessionConfig(BaseConfig):
    bind: Engine
    autoflush: bool | None = Field(default=True)
    expire_on_commit: bool | None = Field(default=False)

    @property
    def session(self):
        return sessionmaker(**vars(self))


session_conf_dict = config_dict.get('sqla_engine_settings', dict())
session_config = SessionConfig(bind=engine_config.engine, **session_conf_dict)
