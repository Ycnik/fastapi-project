"""CLI für das Projekt, damit das Modul als Python-Skript ausgeführt werden kann."""

from soldat.asgi_server import run

__all__ = ["run"]

if __name__ == "__main__":
    run()
