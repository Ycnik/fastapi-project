"""Enum für Familienstand."""

from enum import StrEnum


# StrEnum ab Python 3.11 (2022), abgeleitet von str
class Rang(StrEnum):
    """Enum für Rang."""

    REKRUT = "REKRUT"

    SOLDAT = "SOLDAT"

    ELITE_SOLDAT = "ELITE-SOLDAT"

    CAPTAIN = "CAPTAIN"

    KOMMANDANT = "KOMMANDANT"
