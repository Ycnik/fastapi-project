"""Entity-Klasse für Rechnung."""

from datetime import date

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from soldat.entity.base import Base
from soldat.entity.schweregrad import Schweregrad


class Verletzung(Base):
    """Entity-Klasse für Verletzungen."""

    __tablename__ = "verletzung"

    verletzungsbezeichnung: Mapped[str]
    """die Bezeichnung einer Verletzung."""

    schweregrad: Mapped[Schweregrad]
    """Der grad einer Verletzung."""

    behandelt: Mapped[bool]
    """Wurde diese Verletzung behandelt"""

    verletzungsdatum: Mapped[date]
    """Wann die Verletzung entstand"""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    soldat_id: Mapped[int] = mapped_column(ForeignKey("soldat.id"))
    """ID des zugehörigen Soldaten als Fremdschlüssel in der DB-Tabelle."""

    soldat: Mapped[Soldat] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable ]
        back_populates="verletzung",
    )
    """Das zugehörige transiente Soldaten-Objekt."""

    # __repr__ fuer Entwickler/innen, __str__ fuer User
    def __repr__(self) -> str:
        """Ausgabe der Verletzung als String ohne die Soldatendaten."""
        return (
            f"Verletzung(id={self.id}, "
            + f" verletzunsbezeichnung={self.verletzungsbezeichnung}, "
            + f"schweregrad={self.schweregrad}, behandelt={self.behandelt},"
            + f"verletzungsdatum={self.verletzungsdatum}"
        )
