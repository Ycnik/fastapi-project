"""Pydantic-Model zum Aktualisieren von Soldatendaten."""

from datetime import date
from typing import Annotated, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, StringConstraints

from soldat.entity.geschlecht import Geschlecht
from soldat.entity.rang import Rang
from soldat.entity.soldat import Soldat

__all__ = ["SoldatUpdateModel"]


class SoldatUpdateModel(BaseModel):
    """Pydantic-Model zum Aktualisieren von Soldatendaten."""

    vorname: Annotated[
        str,
        StringConstraints(
            pattern="^[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß])?$",
            max_length=64,
        ),
    ]
    """Der Vorname."""
    nachname: Annotated[
        str,
        StringConstraints(
            pattern="^[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß])?$",
            max_length=64,
        ),
    ]
    """Der Nachname."""
    rang: Rang
    """Der Rang."""
    geburtsdatum: date
    """Das Geburtsdatum."""
    geschlecht: Geschlecht
    """Das Geschlecht."""

    model_config = ConfigDict(
            json_schema_extra={
        "example": {
            "vorname": "Eren",
            "nachname": "Jaeger",
            "rang": "REKRUT",
            "geburtsdatum": "2001-03-30",
            "geschlecht": "M",
        },
    }
)

    def to_dict(self) -> dict[str, Any]:
        """Konvertierung der primitiven Attribute in ein Dictionary.

        :return: Dictionary mit den primitiven Soldat-Attributen
        :rtype: dict[str, Any]
        """
        soldat_dict = self.model_dump()
        soldat_dict["id"] = None
        soldat_dict["ausruestung"] = None
        soldat_dict["verletzungen"] = []
        soldat_dict["username"] = None
        soldat_dict["erzeugt"] = None
        soldat_dict["aktualisiert"] = None

        return soldat_dict

    def to_soldat(self) -> Soldat:
        """Konvertierung in ein Soldat-Objekt für SQLAlchemy.

        :return: Soldat-Objekt für SQLAlchemy
        :rtype: Soldat
        """
        logger.debug("self={}", self)
        soldat_dict = self.to_dict()

        soldat = Soldat(**soldat_dict)
        logger.debug("soldat={}", soldat)
        return soldat
