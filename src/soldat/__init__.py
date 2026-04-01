"""Paket fuer die Soldat-Anwendung."""

from soldat.asgi_server import run
from soldat.fastapi_app import app

__all__ = ["app", "main"]


def main():  # noqa: RUF067
    """main-Funktion, damit das Modul als Skript aufgerufen werden kann."""
    run()
