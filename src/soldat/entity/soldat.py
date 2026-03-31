"""Entity-Klasse für Soldatendaten."""


from datetime import date, datetime
from typing import Any, Self

from sqlalchemy import Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from soldat.entity.base import Base
from soldat.entity.geschlecht import Geschlecht
from soldat.entity.rang import Rang
from soldat.entity.verletzung import Verletzung
from soldat.entity.ausrüstung import Ausrüstung

class Soldat(Base):
    """Entity-Klasse für Soldatendaten."""

    __tablename__ = "soldat"

    vorname: Mapped[str]
    """Der Vorname."""

    nachname: Mapped[str]
    """Der Nachname"""

    rang: Mapped[Rang]
    """Angabe, des Ranges eines Soldaten"""

    geburtsdatum: Mapped[date]
    """Das Geburtsdatum."""

    geschlecht: Mapped[Geschlecht]
    """Das  Geschlecht."""

    #titan: Mapped[Titan | None]
    #"""Angabe, des ggf. Titan eines Soldaten"""


    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""


    ausrüstung: Mapped[Ausrüstung] = relationship(
        back_populates="soldat",
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Die in einer 1:1-Beziehung referenzierte Ausrütung."""

    verletzung: Mapped[list[Verletzung]] = relationship(
        back_populates="soldat",
        cascade="save-update, delete",
    )
    """Die in einer 1:N-Beziehung referenzierten Verletzung."""

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Die Versionsnummer für optimistische Synchronisation."""

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
    """Der Zeitstempel für das initiale INSERT in die DB-Tabelle."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )
    """Der Zeitstempel vom letzen UPDATE in der DB-Tabelle."""

    __mapper_args__ = {"version_id_col": version}

    def set(self, soldat: Self) -> None:
        """Primitive Attributwerte überschreiben, z.B. vor DB-Update.

        :param soldat: Soldat-Objekt mit den aktuellen Daten"""
        self.vorname = soldat.vorname
        self.nachname = soldat.nachname
        self.rang = soldat.rang
        self.geburtsdatum = soldat.geburtsdatum
        self.geschlecht = soldat.geschlecht

    def __eq__(self, other: Any) -> bool:
        """Vergleich auf Gleicheit, ohne Joins zu verursachen."""
        # Vergleich der Referenzen: id(self) == id(other)
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Funktion anhand der ID, ohne Joins zu verursachen."""
        return hash(self.id) if self.id is not None else hash(type(self))

    # __repr__ fuer Entwickler/innen, __str__ fuer User
    def __repr__(self) -> str:
        """Ausgabe eines Soldaten als String, ohne Joins zu verursachen."""
        return (
            f"Soldat(id={self.id}, version={self.version}, "
            + f"vorname={self.vorname}, nachname={self.nachname}, "
            + f"rang={self.rang}, geburtsdatum={self.geburtsdatum}, "
            + f"geschlecht={self.geschlecht}, ausrüstung={self.ausrüstung}, "
            + f"verletzung={self.verletzung}, version={self.version}, "
            + f"erzeugt={self.erzeugt}, aktualisiert={self.aktualisiert}) "
            )