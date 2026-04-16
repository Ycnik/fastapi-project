"""DTO-Klasse für die Ausruestung, insbesondere ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass

import strawberry

from soldat.entity.ausruestung import Ausruestung
from soldat.entity.waffe import Waffe


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class AusruestungDTO:
    """DTO-Klasse für die Ausruestung, insbesondere ohne Decorators für SQLAlchemy."""

    waffe: Waffe
    seriennumer: str

    def __init__(self, ausruestung: Ausruestung) -> None:
        """Initialisierung von AusruestungDTO durch ein Entity-Objekt von Asuruestung.

        :param ausruestung: Ausruestung-Objekt mit Decorators für SQLAlchemy
        """
        self.waffe = ausruestung.waffe
        self.seriennumer = ausruestung.seriennummer
