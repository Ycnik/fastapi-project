"""Repository fuer persistente Soldatendaten."""

from typing import Final

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from soldat.entity import Soldat

__all__ = ["SoldatRepository"]

class SoldatRepository:

    def find_by_id(self, soldat_id: int | None, session: Session) -> Soldat | None:
            """Suche mit der Soldaten-ID.

            :param soldat_id: ID des gesuchten Soldaten
            :param session: Session für SQLAlchemy
            :return: Der gefundene Soldat oder None
            :rtype: Soldat | None
            """
            logger.debug("soldat_id={}", soldat_id)

            if soldat_id is None:
                return None

            statement: Final = (
                select(Soldat)
                .options(joinedload(Soldat.ausrüstung))
                .where(Soldat.id == soldat_id)
            )
            soldat: Final = session.scalar(statement)

            logger.debug("{}", soldat)
            return soldat