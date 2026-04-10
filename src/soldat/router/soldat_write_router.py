"""SoldatWriteRouter."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Response, status
from loguru import logger

from soldat.router.dependencies import get_write_service
from soldat.service import SoldatWriteService

__all__ = ["soldat_write_router"]


soldat_write_router: Final = APIRouter(tags=["Schreiben"])


@soldat_write_router.delete(
    "/{soldat_id}"
)
def delete_by_id(
    soldat_id: int,
    service: Annotated[SoldatWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um einen Soldaten anhand seiner ID zu löschen.

    :param soldat_id: ID des zu löschenden Soldaten
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    """
    logger.debug("soldat_id={}", soldat_id)
    service.delete_by_id(soldat_id=soldat_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
