"""Enum für Schweregrad."""

from enum import StrEnum

# StrEnum ab Python 3.11  (2022), abgeleitet von str
class Schweregrad(StrEnum):
   
    LEICHT = "LEICHT"

    MITTEL = "MITTEL"

    SCHWER = "SCHWER"

    KRITISCH = "KRITISCH"

