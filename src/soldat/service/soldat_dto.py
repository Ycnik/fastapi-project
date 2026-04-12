"""DTO-Klasse für Soldatendaten, insbesondere ohne Decorators für SQLAlchemy."""
from dataclasses import dataclass
from datetime import date

import strawberry

from soldat.entity import Rang, Soldat
from soldat.entity.geschlecht import Geschlecht
from soldat.service.ausruestung_dto import AusruestungDTO
from soldat.service.verletzung_dto import VerletzungDTO

__all__ = ["SoldatDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class SoldatDTO:
    """DTO-Klasse für aus gelesene oder gespeicherte Soldatendaten: ohne Decorators."""

    id: int
    version: int
    vorname: str
    nachname: str
    rang: Rang
    geburtsdatum: date
    geschlecht: Geschlecht
    ausruestung: AusruestungDTO
    verletzungen: list[VerletzungDTO]
    username: str | None

    def __init__(self, soldat: Soldat):
        """Initialisierung von SoldatDTO durch ein Entity-Objekt von Soldat.

        :param soldat: Soldat-Objekt mit Decorators zu SQLAlchemy
        """
        soldat_id = soldat.id
        self.id = soldat_id if soldat_id is not None else -1
        self.version = soldat.version
        self.vorname = soldat.vorname
        self.nachname = soldat.nachname
        self.rang = soldat.rang
        self.geburtsdatum = soldat.geburtsdatum
        self.geschlecht = soldat.geschlecht
        self.ausruestung = AusruestungDTO(soldat.ausruestung)
        self.verletzungen = [VerletzungDTO(v) for v in soldat.verletzungen]
        self.username = soldat.username if soldat.username is not None else "N/A"
