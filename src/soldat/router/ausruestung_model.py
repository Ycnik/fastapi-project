"""Pydantic-Model für die Ausruestung."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from soldat.entity import Ausruestung, Waffe

__all__ = ["AusruestungModel"]


class AusruestungModel(BaseModel):
    """Pydantic-Model für die ausruestung_dict."""

    waffe: Waffe
    """Die Waffe."""
    seriennummer: Annotated[str, StringConstraints(
        max_length=64,
        pattern=r"^AOT-[A-Za-z0-9]+$",
    )]
    """Die Seriennummer."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "waffe": "ODM_GEAR",
                "seriennummer": "AOT-G3612345",
            },
        }
    )

    def to_ausruestung(self) -> Ausruestung:
        """Konvertierung in ein Ausruestung-Objekt für SQLAlchemy.

        :return: Ausruestung-Objekt für SQLAlchemy
        :rtype: Ausruestung
        """
        ausruestung_dict = self.model_dump()
        ausruestung_dict["id"] = None
        ausruestung_dict["soldat_id"] = None
        ausruestung_dict["soldat"] = None

        return Ausruestung(**ausruestung_dict)
