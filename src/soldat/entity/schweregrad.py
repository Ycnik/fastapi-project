"""Enum für Schweregrad."""

from enum import StrEnum


# StrEnum ab Python 3.11  (2022), abgeleitet von str
class Schweregrad(StrEnum):
    """Enum fuer den Schweregrad einer Verletzung."""

    LEICHT = "LEICHT"

    MITTEL = "MITTEL"

    SCHWER = "SCHWER"

    KRITISCH = "KRITISCH"
