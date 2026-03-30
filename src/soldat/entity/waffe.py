"""Enum für Ausrüstungstyp."""

from enum import StrEnum

# StrEnum ab Python 3.11 (2022), abgeleitet von str
# zusaetzlich als enum fuer das GraphQL-Schema
class Waffe(StrEnum):
    """Enum für Waffe."""

    ODM_GEAR = "ODM_GEAR"

    Schrotflinte = "Schrotflinte"

    Klinge = "Klingen"

