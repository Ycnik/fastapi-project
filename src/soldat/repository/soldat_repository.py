"""Repository fuer persistente Soldatendaten."""

from typing import Final

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from soldat.entity import Soldat

__all__ = ["SoldatRepository"]


class SoldatRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Patient."""

    def find_by_id(self, soldaten_id: int | None, session: Session) -> Soldat | None:
        """Suche mit der Soldaten-ID.

        :param soldat_id: ID des gesuchten Soldaten
        :param session: Session für SQLAlchemy
        :return: Der gefundene Soldat oder None
        :rtype: Soldat | None
        """
        logger.debug("soldat_id={}", soldaten_id)

        if soldaten_id is None:
            return None

        statement: Final = (
            select(Soldat)
            .options(joinedload(Soldat.ausruestung))
            .where(Soldat.id == soldaten_id)
        )
        soldat: Final = session.scalar(statement)

        logger.debug("{}", soldat)
        return soldat
