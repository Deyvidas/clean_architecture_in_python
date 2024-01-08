from config import config_dict
from config.base_config import BaseConfig


class PostgreSQLConfig(BaseConfig):
    """Model which represent PostgreSQL configuration."""

    dialect_driver: str
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    @property
    def url(self) -> str:
        url = '{core}://{username}:{password}@{host}:{port}/{db_name}'
        return url.format(
            core=self.dialect_driver,
            username=self.db_username,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            db_name=self.db_name,
        )


postgresql_conf_dict = config_dict.get('postgresql', dict())
postgresql_config = PostgreSQLConfig(**postgresql_conf_dict)
