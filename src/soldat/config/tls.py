"""Konfiguration für den privaten Schlüssel und das Zertifikat für TLS."""

from importlib.resources import files
from typing import TYPE_CHECKING, Final

from loguru import logger

from soldat.config.config import app_config, resources_path

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

__all__ = ["tls_certfile", "tls_keyfile"]


_tls_toml: Final = app_config.get("tls", {})
_tls_path: Final[Traversable] = files(resources_path) / "tls"

_key: Final[str] = _tls_toml.get("key", "key.pem")
tls_keyfile: Final[str] = str(_tls_path / _key)
logger.debug("private keyfile TLS: {}", tls_keyfile)

_certificate: Final[str] = _tls_toml.get("certificate", "certificate.crt")
tls_certfile: Final[str] = str(_tls_path / _certificate)
logger.debug("certfile TLS: {}", tls_certfile)
