"""Geschäftslogik zum Lesen von Soldatenendaten."""
from typing import Final
from soldat.repository import Session, SoldatRepository
from loguru import logger
from soldat.service.exceptions import NotFoundError
from soldat.service.soldat_dto import SoldatDTO

__all__ = ["SoldatService"]
class SoldatService:
    """Service-Klasse mit Geschäftslogik für Soldat."""

    def __init__(self, repo: SoldatRepository) -> None:
        """Konstruktor mit abhängigem SoldatenRepository."""
        self.repo: SoldatRepository = repo

    def find_by_id(self, soldat_id: int) -> SoldatDTO:
            """Suche mit der Soldaten-ID.

            :param soldat_id: ID für die Suche
            :param user: User aus dem Token
            :return: Der gefundene Soldat
            :rtype: SoldatenDTO
            :raises NotFoundError: Falls kein Soldat gefunden
            :raises ForbiddenError: Falls die Soldatendaten nicht gelesen werden dürfen
            """
            logger.debug("soldat_id={}, user={}", soldat_id)

            with Session() as session:

                if (
                    soldat := self.repo.find_by_id(soldat_id=soldat_id, session=session)
                ) is None:
                    raise NotFoundError(soldat_id=soldat_id)

                soldat_dto: Final = SoldatDTO(soldat)
                session.commit()

            logger.debug("{}", soldat_dto)
            return soldat_dto