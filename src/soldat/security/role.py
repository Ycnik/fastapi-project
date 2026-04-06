"""Enum für Rollen."""

from enum import StrEnum


class Role(StrEnum):
    """Enum für Rollen."""

    ADMIN = "ADMIN"
    """Rolle für die Administration."""

    SOLDAT = "SOLDAT"
    """Rolle registrierter Patient."""
