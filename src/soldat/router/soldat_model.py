"""Pydantic-Model für die Soldatendaten."""

from typing import Annotated, Final

from loguru import logger
from pydantic import StringConstraints

from soldat.entity import Soldat
from soldat.router.ausruestung_model import AusruestungModel
from soldat.router.soldat_update_model import SoldatUpdateModel
from soldat.router.verletzung_model import VerletzungModel

__all__ = ["SoldatModel"]


# https://towardsdatascience.com/pydantic-or-dataclasses-why-not-both-convert-between-them-ba382f0f9a9c
class SoldatModel(SoldatUpdateModel):
    """Pydantic-Model für die Soldatendaten."""

    ausruestung: AusruestungModel
    """Die zugehörige Ausruestung."""
    verletzungen: list[VerletzungModel]
    """Die Liste der Verletzungen."""
    username: Annotated[str, StringConstraints(max_length=20)]
    """Der Benutzername für Login."""

    def to_soldat(self) -> Soldat:
        """Konvertierung in ein Soldat-Objekt für SQLAlchemy.

        :return: Soldat-Objekt für SQLAlchemy
        :rtype: Soldat
        """
        logger.debug("self={}", self)
        soldat_dict = self.to_dict()
        soldat_dict["username"] = self.username

        soldat: Final = Soldat(**soldat_dict)
        soldat.ausruestung = self.ausruestung.to_ausruestung()
        soldat.verletzungen = [
            verletzung_model.to_verletzung() for verletzung_model in self.verletzungen
        ]
        logger.debug("soldat={}", soldat)
        return soldat
