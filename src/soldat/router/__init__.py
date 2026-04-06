"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from soldat.router.soldat_router import soldat_router

__all__: Sequence[str] = [
    "soldat_router",
]
