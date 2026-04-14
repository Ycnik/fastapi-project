"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from soldat.router.health_router import router as health_router
from soldat.router.soldat_router import soldat_router
from soldat.router.soldat_write_router import soldat_write_router

__all__: Sequence[str] = [
    "health_router",
    "soldat_router",
    "soldat_write_router",
]
