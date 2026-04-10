"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from soldat.repository.soldat_repository import SoldatRepository
from soldat.service.soldat_service import SoldatService
from soldat.service.soldat_write_service import SoldatWriteService


def get_repository() -> SoldatRepository:
    """Factory-Funktion für SoldatRepository.

    :return: Das Repository
    :rtype: SoldatRepository
    """
    return SoldatRepository()


def get_service(
    repo: Annotated[SoldatRepository, Depends(get_repository)],
) -> SoldatService:
    """Factory-Funktion für SoldatService."""
    return SoldatService(repo=repo)


def get_write_service(
    repo: Annotated[SoldatRepository, Depends(get_repository)],
) -> SoldatWriteService:
    """Factory-Funktion für PatientWriteService."""
    return SoldatWriteService(repo=repo)
