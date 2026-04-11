"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from soldat.router.soldat_router import soldat_router
from soldat.router.soldat_write_router import soldat_write_router

__all__: Sequence[str] = [
    "soldat_router",
    "soldat_write_router",
]
