"""Entity-Klasse für die Ausrüstung."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from soldat.entity.base import Base
from soldat.entity.waffe import Waffe

class Ausrüstung(Base):
    """Entity-Klasse für die Ausrüstung."""

    __tablename__ = "ausrüstung"

    waffe: Mapped[Waffe]
    """Die Waffe."""

    seriennummer: Mapped[str]
    """Die Seriennummer."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    soldat: Mapped[int] = mapped_column(ForeignKey("soldat.id"))
    """ID des zugehörigen Soldaten als Fremdschlüssel in der DB-Tabelle."""

    soldat: Mapped[Soldat] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
        back_populates="ausrüstung",
    )
    """Das zugehörige transiente Soldaten-Objekt."""

    # __repr__ fuer Entwickler/innen, __str__ fuer User
    def __repr__(self) -> str:
        """Ausgabe einer Ausrüstung als String ohne die Soldatenndaten."""
        return f"Ausrüstung(id={self.id}, waffe={self.waffe}, seriennummer={self.seriennummer})"
