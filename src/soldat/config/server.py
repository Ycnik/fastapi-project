"""Konfiguration für ASGI."""

from typing import Final

from soldat.config.config import app_config

__all__ = ["host_binding", "port"]


_server_toml: Final = app_config.get("server", {})

host_binding: Final[str] = _server_toml.get("host-binding", "127.0.0.1")
"""'Host Binding', z.B. 127.0.0.1 (default) oder 0.0.0.0."""

port: Final[int] = _server_toml.get("port", 8000)
"""Port für den Server (default: 8000)."""

reload: Final[bool] = bool(_server_toml.get("reload", False))
