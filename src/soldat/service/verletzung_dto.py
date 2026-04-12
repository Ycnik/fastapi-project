"""DTO-Klasse für die Verletzung, insbesondere ohne Decorators für SQLAlchemy."""
from dataclasses import dataclass
from datetime import date

import strawberry

from soldat.entity import Schweregrad, Verletzung


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class VerletzungDTO:
    """DTO-Klasse für die Verletzung, insbesondere ohne Decorators für SQLAlchemy."""

    verletzungsbezeichnung: str
    schweregrad: Schweregrad
    behandelt: bool
    verletzungsdatum: date

    def __init__(self, verletzung: Verletzung) -> None:
        """Initialisierung von VerletzungDTO durch ein Entity-Objekt von Verletzung.

        :param verletzug: Verletzung-Objekt mit Decorators für SQLAlchemy
        """
        self.verletzungsbezeichnung = verletzung.verletzungsbezeichnung
        self.schweregrad = verletzung.schweregrad
        self.behandelt = verletzung.behandelt
        self.verletzungsdatum = verletzung.verletzungsdatum
