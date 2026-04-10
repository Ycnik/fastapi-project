"""Geschäftslogik zum Schreiben von Soldatendaten."""
from typing import Final

from loguru import logger

from soldat.entity import Soldat
from soldat.repository import Session, SoldatRepository
from soldat.service.soldat_dto import SoldatDTO

__all__ = ["SoldatWriteService"]


class SoldatWriteService:
    """Service-Klasse mit Geschäftslogik für Soldat."""

    def __init__(self, repo: SoldatRepository) -> None:
        """Konstruktor mit abhaengigem SoldatRepository."""
        self.repo: SoldatRepository = repo

    def create(self, soldat: Soldat) -> SoldatDTO:
        """Einen neuen Soldaten anlegen.

        :param soldat: Der neue Soldat ohne ID
        :return: Der neu angelegte Soldat mit generierter ID
        :rtype: SoldatDTO
        """
        logger.debug(
            "soldat={}, ausruestung={}, verletzungen={}",
            soldat,
            soldat.ausruestung,
            soldat.verletzungen,
        )

        with Session() as session:

            soldat_db: Final = self.repo.create(soldat=soldat, session=session)
            soldat_dto: Final = SoldatDTO(soldat_db)
            session.commit()

        logger.debug("soldat_dto={}", soldat_dto)
        return soldat_dto
