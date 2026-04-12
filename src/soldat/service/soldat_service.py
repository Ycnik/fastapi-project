"""Geschäftslogik zum Lesen von Soldatenendaten."""

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Final

from loguru import logger
from openpyxl import Workbook

from soldat.config.excel import excel_enabled
from soldat.repository import Pageable, Session, Slice, SoldatRepository
from soldat.security.role import Role
from soldat.security.user import User
from soldat.service.exceptions import ForbiddenError, NotFoundError
from soldat.service.soldat_dto import SoldatDTO

__all__ = ["SoldatService"]


class SoldatService:
    """Service-Klasse mit Geschäftslogik für Soldat."""

    def __init__(self, repo: SoldatRepository) -> None:
        """Konstruktor mit abhängigem SoldatenRepository."""
        self.repo: SoldatRepository = repo

    def find_by_id(self, soldat_id: int, user: User) -> SoldatDTO:
        """Suche mit der Soldaten-ID.

        :param soldat_id: ID fuer die Suche
        :param user: User aus dem Token
        :return: Der gefundene Soldat
        :rtype: SoldatDTO
        :raises NotFoundError: Falls kein Soldat gefunden
        :raises ForbiddenError: Falls die Soldatendaten nicht gelesen werden dürfen
        """
        logger.debug("soldat_id={}, user={}", soldat_id, user)

        with Session() as session:
            user_is_admin: Final = Role.ADMIN in user.roles

            if (soldat := self.repo.find_by_id(soldat_id=soldat_id, session=session)
            ) is None:
                if user_is_admin:
                    message: Final = f"Kein Soldat mit der ID {soldat_id}"
                    logger.debug("NotFoundError: {}", message)
                    # "Throw Exceptions Instead of Returning Errors"
                    raise NotFoundError(soldat_id=soldat_id)
                logger.debug("nicht admin")
                raise ForbiddenError

            if soldat.username != user.username and not user_is_admin:
                logger.debug(
                    "soldat.username={}, user.username={}, user.roles={}",
                    soldat.username,
                    user.username,
                    user.roles,
                )
                raise ForbiddenError

            soldat_dto: Final = SoldatDTO(soldat)
            session.commit()

        logger.debug("{}", soldat_dto)
        return soldat_dto

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
    ) -> Slice[SoldatDTO]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter
        :return: Liste der gefundenen Soldaten
        :rtype: Slice[SoldatDTO]
        :raises NotFoundError: Falls keine Soldaten gefunden wurden
        """
        logger.debug("{}", suchparameter)
        with Session() as session:
            soldat_slice: Final = self.repo.find(
                suchparameter=suchparameter, pageable=pageable, session=session
            )
            if len(soldat_slice.content) == 0:
                raise NotFoundError(suchparameter=suchparameter)

            soldaten_dto: Final = tuple(
                SoldatDTO(soldat) for soldat in soldat_slice.content
            )
            session.commit()

        if excel_enabled:
            self._create_excelsheet(soldaten_dto)
        soldaten_dto_slice = Slice(
            content=soldaten_dto, total_elements=soldat_slice.total_elements
        )
        logger.debug("{}", soldaten_dto_slice)
        return soldaten_dto_slice

    def find_nachnamen(self, teil: str) -> Sequence[str]:
        """Suche Nachnamen zu einem Teilstring.

        :param teil: Teilstring der gesuchten Nachnamen
        :return: Liste der gefundenen Nachnamen oder eine leere Liste
        :rtype: list[str]
        :raises NotFoundError: Falls keine Nachnamen gefunden wurden
        """
        logger.debug("teil={}", teil)
        with Session() as session:
            nachnamen: Final = self.repo.find_nachnamen(teil=teil, session=session)
            session.commit()

            logger.debug("{}", nachnamen)
            if len(nachnamen) == 0:
                raise NotFoundError
            return nachnamen

    def _create_excelsheet(self, soldaten: tuple[SoldatDTO, ...]) -> None:
        """Ein Excelsheet mit den gefundenen Soldaten erstellen.

        :param soldaten: Soldatenendaten für das Excelsheet
        """
        workbook: Final = Workbook()
        worksheet: Final = workbook.active
        if worksheet is None:
            return

        worksheet.append(["Vorname", "Nachname", "Ausruestung", "Verletzung"])
        for soldat in soldaten:
            ausruestung = (
                str(soldat.ausruestung) if soldat.ausruestung is not None else "N/A"
            )
            verletzung = (
                str(soldat.verletzungen) if soldat.verletzungen is not None else "N/A"
            )
            worksheet.append((
                soldat.vorname,
                soldat.nachname,
                ausruestung,
                verletzung,
            ))

        timestamp: Final = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        workbook.save(f"soldaten-{timestamp}.xlsx")
