"""Pydantic-Model für eine Verletzung."""

from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from soldat.entity import Schweregrad, Verletzung

__all__ = ["VerletzungModel"]


class VerletzungModel(BaseModel):
    """Pydantic-Model für eine Verletzung."""

    verletzungsbezeichnung: Annotated[str, StringConstraints(max_length=64)]
    """Verletzungsbezeichnung"""
    schweregrad: Schweregrad
    """Schweregrad"""
    behandelt: bool
    """Behandelt ja/nein"""
    verletzungsdatum: date
    """Verletzungsdatum"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "verletzungsbezeichnung": "Verbrennung",
                "schweregrad": "SCHWER",
                "behandelt": True,
                "verletzungsdatum": "2005-08-25",
            },
        }
    )

    def to_verletzung(self) -> Verletzung:
        """Konvertierung in ein Verletzung-Objekt für SQLAlchemy.

        :return: Verletzung-Objekt für SQLAlchemy
        :rtype: Verletzung
        """
        verletzung_dict = self.model_dump()
        verletzung_dict["id"] = None
        verletzung_dict["soldat_id"] = None
        verletzung_dict["soldat"] = None
        return Verletzung(**verletzung_dict)
