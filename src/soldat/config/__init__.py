"""Modul zur Konfiguration."""

from soldat.config.server import host_binding, port
from soldat.config.tls import tls_certfile, tls_keyfile

__all__ = [
    "host_binding",
    "port",
    "tls_certfile",
    "tls_keyfile",
]
