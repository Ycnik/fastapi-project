"""Enum für Ausrüstungstyp."""

from enum import StrEnum

import strawberry


# StrEnum ab Python 3.11 (2022), abgeleitet von str
# zusaetzlich als enum fuer das GraphQL-Schema
@strawberry.enum
class Waffe(StrEnum):
    """Enum für Waffe."""

    ODM_GEAR = "ODM_GEAR"

    Schrotflinte = "Schrotflinte"

    Klinge = "Klingen"

