"""Geschäftslogik zum Schreiben von Soldatendaten."""
from typing import Final

from loguru import logger

from soldat.entity import Soldat
from soldat.repository import Session, SoldatRepository
from soldat.service.exceptions import (
    NotFoundError,
    VersionOutdatedError,
)
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

    def update(self, soldat: Soldat, soldat_id: int, version: int) -> SoldatDTO:
        """Daten eines Soldaten ändern.

        :param soldat: Die neuen Daten
        :param soldat_id: ID des zu aktualisierenden Soldaten
        :param version: Version für optimistische Synchronisation
        :return: Der aktualisierte Soldat
        :rtype: SoldatDTO
        :raises NotFoundError: Falls der zu aktualisierende Soldat nicht existiert
        :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
        """
        logger.debug("soldat_id={}, version={}, {}", soldat_id, version, soldat)

        with Session() as session:
            if (
                soldat_db := self.repo.find_by_id(
                    soldat_id=soldat_id, session=session
                )
            ) is None:
                raise NotFoundError(soldat_id)
            if soldat_db.version > version:
                raise VersionOutdatedError(version)

            soldat_db.set(soldat)
            if (
                soldat_updated := self.repo.update(soldat=soldat_db, session=session)
            ) is None:
                raise NotFoundError(soldat_id)
            soldat_dto: Final = SoldatDTO(soldat_updated)
            logger.debug("{}", soldat_dto)

            session.commit()
            soldat_dto.version += 1
            return soldat_dto

    def delete_by_id(self, soldat_id: int) -> None:
        """Einen Soldaten anhand seiner ID löschen.

        :param soldat_id: ID des zu löschenden Soldaten
        """
        logger.debug("soldat_id={}", soldat_id)
        with Session() as session:
            self.repo.delete_by_id(soldat_id=soldat_id, session=session)
            session.commit()
