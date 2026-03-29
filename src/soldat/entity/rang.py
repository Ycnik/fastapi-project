"""Enum für Familienstand."""

from enum import StrEnum

import strawberry


# StrEnum ab Python 3.11 (2022), abgeleitet von str
@strawberry.enum
class Rang(StrEnum):
    """Enum für Rang."""

    REKRUT = "REKRUT"

    SOLDAT = "SOLDAT"

    ELITE_SOLDAT = "ELITE-SOLDAT"

    CAPTAIN = "CAPTAIN"

    KOMMANDANT = "KOMMANDANT"

