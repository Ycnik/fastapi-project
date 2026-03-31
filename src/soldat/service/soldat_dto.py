"""DTO-Klasse für Patientendaten, insbesondere ohne Decorators für SQLAlchemy."""

from datetime import date

from soldat.entity import Rang, Soldat, Verletzung
from soldat.entity.ausruestung import Ausruestung
from soldat.entity.geschlecht import Geschlecht


class SoldatDTO:
    """DTO-Klasse für aus gelesene oder gespeicherte Patientendaten: ohne Decorators."""

    id: int
    version: int
    vorname: str
    nachname: str
    rang: Rang
    geburtsdatum: date
    geschlecht: Geschlecht
    ausruestung: Ausruestung
    verletzungen: list[Verletzung]

    def __init__(self, soldat: Soldat):
        """Initialisierung von PatientDTO durch ein Entity-Objekt von Patient.

        :param patient: Patient-Objekt mit Decorators zu SQLAlchemy
        """
        soldat_id = soldat.id
        self.id = soldat_id if soldat_id is not None else -1
        self.version = soldat.version
        self.vorname = soldat.vorname
        self.nachname = soldat.nachname
        self.rang = soldat.rang
        self.geburtsdatum = soldat.geburtsdatum
        self.geschlecht = soldat.geschlecht
        self.ausruestung = soldat.ausruestung
        self.verletzungen = soldat.verletzungen
