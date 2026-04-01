"""DB-URL erstellen."""

from importlib.resources import files
from typing import TYPE_CHECKING, Final, Literal

from loguru import logger
from sqlalchemy.engine import URL

from soldat.config.config import app_config, resources_path

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

__all__ = [
    "db_connect_args",
    "db_dialect",
    "db_log_statements",
    "db_url",
    "db_url_admin",
]

_db_toml: Final = app_config.get("db", {})

db_dialect: Final[Literal["postgresql"]] = _db_toml.get(
    "dialect",
    "postgresql",
)
"""DB-Dialekt für SQLAlchemy: 'postgresql'."""
logger.debug("db: db_dialect={}", db_dialect)

_drivername = "postgresql+psycopg"
_dbname: Final[str] = _db_toml.get("name", "soldat")
_host: Final[str] = _db_toml.get("host", "postgres")
_username: Final[str] = _db_toml.get("username", "soldat")
_password: Final[str] = _db_toml.get("password", "Change Me!")
_password_admin: Final[str] = _db_toml.get("password-admin", "Change Me!")

db_log_statements: Final[bool] = bool(_db_toml.get("log-statements", False))
"""True, falls die SQL-Anweisungen protokolliert werden sollen."""

db_url: Final[URL] = URL.create(
    drivername=_drivername,
    username=_username,
    password=_password,
    host=_host,
    database=_dbname,
)
"""DB-URL für SQLAlchemy."""
logger.debug("db: db_url={}", db_url)

db_url_admin: Final[URL] = URL.create(
    drivername=_drivername,
    username="postgres",
    password=_password_admin,
    host=_host,
    database=_dbname,
)
"""DB-URL für den Superuser für SQLAlchemy."""


def _create_connect_args() -> dict[str, str | dict[str, str]] | None:
    db_resources_traversable: Final[Traversable] = files(resources_path)

    cafile: Final = str(
        db_resources_traversable / db_dialect / "server.crt",
    )
    return {
        "sslmode": "verify-full",  # oder "require" oder "prefer"
        "sslrootcert": cafile,
    }


db_connect_args: dict[str, str | dict[str, str]] | None = _create_connect_args()
"""Schlüssel-Wert-Paare für TLS bei PostgreSQL."""
logger.debug("db: db_connect_args={}", db_connect_args)
