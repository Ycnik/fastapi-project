"""Repository fuer persistente Soldatendaten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from soldat.entity import Ausruestung, Soldat
from soldat.repository.pageable import Pageable
from soldat.repository.slice import Slice

__all__ = ["SoldatRepository"]


class SoldatRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Soldat."""

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
            .options(joinedload(Soldat.ausruestung), joinedload(Soldat.verletzungen))
            .where(Soldat.id == soldat_id)
        )
        soldat: Final = session.scalar(statement)

        logger.debug("{}", soldat)
        return soldat

    def find_nachnamen(self, teil: str, session: Session) -> Sequence[str]:
        """Suche Nachnamen zu einem Teilstring.

        :param teil: Teilstring zu den gesuchten Nachnamen
        :param session: Session für SQLAlchemy
        :return: Liste der gefundenen Nachnamen oder eine leere Liste
        :rtype: Sequence[str]
        """
        logger.debug("teil={}", teil)

        statement: Final = (
            select(Soldat.nachname)
            .filter(Soldat.nachname.ilike(f"%{teil}%"))
            .distinct()
        )
        nachnamen: Final = (session.scalars(statement)).all()

        logger.debug("nachnamen={}", nachnamen)
        return nachnamen

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[Soldat]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter als Dictionary
        :param pageable: Anzahl Datensätze und Seitennummer
        :param session: Session für SQLAlchemy
        :return: Tupel, d.h. readonly Liste, der gefundenen Soldaten oder leeres Tupel
        :rtype: Slice[Soldat]
        """
        log_str: Final = "{}"
        logger.debug(log_str, suchparameter)
        if not suchparameter:
            return self._find_all(pageable=pageable, session=session)

        # Iteration ueber die Schluessel des Dictionaries mit den Suchparameter
        for key, value in suchparameter.items():
            if key == "nachname":
                soldaten = self._find_by_nachname(
                    teil=value, pageable=pageable, session=session
                )
                logger.debug(log_str, soldaten)
                return soldaten
        return Slice(content=(), total_elements=0)

    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Soldat]:
        logger.debug("aufgerufen")
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Soldat)
                .options(
                    joinedload(Soldat.ausruestung), joinedload(Soldat.verletzungen)
                )
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Soldat).options(
                    joinedload(Soldat.ausruestung), joinedload(Soldat.verletzungen)
                )
            )
        )
        soldaten: Final = (session.scalars(statement)).all()
        anzahl: Final = self._count_all_rows(session)
        soldat_slice: Final = Slice(content=tuple(soldaten), total_elements=anzahl)
        logger.debug("soldat_slice={}", soldat_slice)
        return soldat_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Soldat)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_nachname(
        self,
        teil: str,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Soldat]:
        logger.debug("teil={}", teil)
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Soldat)
                .options(
                    joinedload(Soldat.ausruestung), joinedload(Soldat.verletzungen)
                )
                .filter(Soldat.nachname.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Soldat)
                .options(
                    joinedload(Soldat.ausruestung), joinedload(Soldat.verletzungen)
                )
                .filter(Soldat.nachname.ilike(f"%{teil}%"))
            )
        )
        soldaten: Final = session.scalars(statement).unique().all()
        anzahl: Final = self._count_rows_nachname(teil, session)
        soldat_slice: Final = Slice(content=tuple(soldaten), total_elements=anzahl)
        logger.debug("{}", soldat_slice)
        return soldat_slice

    def _count_rows_nachname(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Soldat)
            .filter(Soldat.nachname.ilike(f"%{teil}%"))
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def exists_seriennummer(self, seriennummer: str, session: Session) -> bool:
        """Prüfen, ob eine Seriennummer bereits existiert.

        :param seriennummer: Zu prüfende Seriennummer
        :param session: Session für SQLAlchemy
        :return: True, falls die Seriennummer bereits existiert, sonst False
        :rtype: bool
        """
        logger.debug("seriennummer={}", seriennummer)
        statement: Final = (
            select(func.count())
            .select_from(Ausruestung)
            .where(Ausruestung.seriennummer == seriennummer)
        )
        anzahl: Final = session.scalar(statement)
        logger.debug("anzahl={}", anzahl)
        return anzahl is not None and anzahl > 0

    def exists_seriennummer_other_id(
        self,
        seriennummer: str,
        soldat_id: int,
        session: Session,
    ) -> bool:
        """Prüfen, ob eine Seriennummer bei einem anderen Soldaten existiert.

        :param seriennummer: Zu prüfende Seriennummer
        :param soldat_id: Eigene Soldat-ID
        :param session: Session für SQLAlchemy
        :return: True, falls die Seriennummer bei einem anderen Soldaten existiert
        :rtype: bool
        """
        logger.debug("seriennummer={}", seriennummer)
        statement: Final = (
            select(Ausruestung.soldat_id)
            .where(Ausruestung.seriennummer == seriennummer)
        )
        soldat_id_db: Final = session.scalar(statement)
        logger.debug("soldat_id_db={}", soldat_id_db)
        return soldat_id_db is not None and soldat_id_db != soldat_id

    def create(self, soldat: Soldat, session: Session) -> Soldat:
        """Speichere einen neuen Soldaten ab.

        :param soldat: Die Daten des neuen Soldaten ohne ID
        :param session: Session für SQLAlchemy
        :return: Der neu angelegte Soldat mit generierter ID
        :rtype: Soldat
        """
        logger.debug(
            "soldat={}, soldat.ausruestung={}, soldat.verletzungen={}",
            soldat,
            soldat.ausruestung,
            soldat.verletzungen,
        )
        session.add(instance=soldat)
        session.flush(objects=[soldat])
        logger.debug("soldat_id={}", soldat.id)
        return soldat

    def update(self, soldat: Soldat, session: Session) -> Soldat | None:
        """Aktualisiere einen Soldaten.

        :param soldat: Die neuen Soldatendaten
        :param session: Session für SQLAlchemy
        :return: Der aktualisierte Soldat oder None, falls kein Soldat mit der ID
        existiert
        :rtype: Soldat | None
        """
        logger.debug("{}", soldat)

        if (
            soldat_db := self.find_by_id(soldat_id=soldat.id, session=session)
        ) is None:
            return None

        logger.debug("{}", soldat_db)
        return soldat_db

    def delete_by_id(self, soldat_id: int, session: Session) -> None:
        """Lösche die Daten zu einem Soldaten.

        :param soldat_id: Die ID des zu löschenden Soldaten
        :param session: Session für SQLAlchemy
        """
        logger.debug("soldat_id={}", soldat_id)

        if (soldat := self.find_by_id(soldat_id=soldat_id, session=session)) is None:
            return
        session.delete(soldat)
        logger.debug("ok")
