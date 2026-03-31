"""SoldatGetRouter."""
from dataclasses import asdict
from typing import Annotated, Final, Any

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from soldat.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from soldat.router.dependencies import get_service
from soldat.service import SoldatDTO, SoldatService

__all__ = ["soldat_router"]


# APIRouter auf Basis der Klasse Router von Starlette
soldat_router: Final = APIRouter(tags=["Lesen"])


@soldat_router.get(
    "/{soldat_id}"
)
def get_by_id(
    soldat_id: int,
    request: Request,
    service: Annotated[SoldatService, Depends(get_service)],
) -> Response:
    """Suche mit der Soldaten-ID.

    :param soldat_id: ID des gesuchten Soldaten als Pfadparameter
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit ggf. If-None-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit dem gefundenen Soldatendatensatz
    :rtype: Response
    :raises NotFoundError: Falls kein Soldat gefunden wurde
    :raises ForbiddenError: Falls die Soldatendaten nicht gelesen werden dürfen
    """
    soldat: Final = service.find_by_id(soldat_id=soldat_id)
    logger.debug("{}", soldat)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)
        if version is not None:
            try:
                if int(version) == soldat.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                logger.debug("invalid version={}", version)

    return JSONResponse(
        content=_soldat_to_dict(soldat),
        headers={ETAG: f'"{soldat.version}"'},
    )


def _soldat_to_dict(soldat: SoldatDTO) -> dict[str, Any]:
    soldat_dict: Final = asdict(obj=soldat)
    soldat_dict.pop("version")
    return soldat_dict