"""Enum für Geschlecht."""

from enum import StrEnum

import strawberry


# StrEnum ab Python 3.11 (2022), abgeleitet von str
# zusaetzlich als enum fuer das GraphQL-Schema
@strawberry.enum
class Geschlecht(StrEnum):
    """Enum für Geschlecht."""

    MAENNLICH = "M"
    """Männlich."""

    WEIBLICH = "W"
    """Weiblich."""
