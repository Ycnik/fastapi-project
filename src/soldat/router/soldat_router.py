"""SoldatGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger

from soldat.repository import Pageable
from soldat.repository.slice import Slice
from soldat.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from soldat.router.dependencies import get_service
from soldat.router.page import Page
from soldat.security import Role, RolesRequired, User
from soldat.service import SoldatDTO, SoldatService

__all__ = ["soldat_router"]


# APIRouter auf Basis der Klasse Router von Starlette
soldat_router: Final = APIRouter(tags=["Lesen"])


@soldat_router.get(
    "/{soldat_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.SOLDAT]))],
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
    user: Final[User] = request.state.current_user
    logger.debug("soldat_id={}, user={}", soldat_id, user)

    soldat: Final = service.find_by_id(soldat_id=soldat_id, user=user)
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


@soldat_router.get(
    "/nachnamen/{teil}",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get_nachnamen(
    teil: str,
    service: Annotated[SoldatService, Depends(get_service)],
) -> JSONResponse:
    """Suche Nachnamen zum gegebenen Teilstring.

    :param teil: Teilstring der gefundenen Nachnamen
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 200 und gefundenen Nachnamen im Body
    :rtype: Response
    :raises NotFoundError: Falls keine Nachnamen gefunden wurden
    """
    logger.debug("teil={}", teil)
    nachnamen: Final = service.find_nachnamen(teil=teil)
    return JSONResponse(content=nachnamen)


def _soldat_to_dict(soldat: SoldatDTO) -> dict[str, Any]:
    soldat_dict: Final = asdict(obj=soldat)
    soldat_dict.pop("version")
    return jsonable_encoder(soldat_dict)


def _soldat_slice_to_page(
    soldat_slice: Slice[SoldatDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    soldat_dict: Final = tuple(
        _soldat_to_dict(soldat) for soldat in soldat_slice.content
    )
    page: Final = Page.create(
        content=soldat_dict,
        pageable=pageable,
        total_elements=soldat_slice.total_elements,
    )
    return asdict(obj=page)


@soldat_router.get(
    "",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get(
    request: Request,
    service: Annotated[SoldatService, Depends(get_service)],
) -> JSONResponse:
    """Suche mit Query-Parameter.

    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit Query-Parameter
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit einer Seite mit Soldaten-Daten
    :rtype: Response
    :raises NotFoundError: Falls keine Soldaten gefunden wurden
    """
    query_params: Final = request.query_params
    log_str: Final = "{}"
    logger.debug(log_str, query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    if "page" in query_params:
        del suchparameter["page"]
    if "size" in query_params:
        del suchparameter["size"]

    soldat_slice: Final = service.find(suchparameter=suchparameter, pageable=pageable)

    result: Final = _soldat_slice_to_page(soldat_slice, pageable)
    logger.debug(log_str, result)
    return JSONResponse(content=result)
