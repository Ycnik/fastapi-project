"""Entity-Klasse für Patientendaten."""
from soldat.entity.ausrüstung import Ausrüstung

from dataclasses import InitVar
from datetime import date, datetime
from typing import Any, Self

from loguru import logger
from sqlalchemy import JSON, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, reconstructor, relationship

from soldat.entity.base import Base
from soldat.entity.titan import Titan
from soldat.entity.geschlecht import Geschlecht
from soldat.entity.rang import Rang

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

    titan: Mapped[Titan | None]
    """Angabe, des ggf. Titan eines Soldaten"""


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
