"""SoldatWriteRouter."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from soldat.problem_details import create_problem_details
from soldat.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from soldat.router.dependencies import get_write_service
from soldat.router.soldat_model import SoldatModel
from soldat.router.soldat_update_model import SoldatUpdateModel
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


@soldat_write_router.post("")
def post(
    soldat_model: SoldatModel,
    request: Request,
    service: Annotated[SoldatWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um einen neuen Soldaten anzulegen.

    :param soldat_model: Soldatendaten als Pydantic-Model
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit der Request-URL
    :param service: Injizierter Service für Geschäftslogik
    :rtype: Response
    :raises ValidationError: Falls es bei Pydantic Validierungsfehler gibt
    """
    logger.debug("soldat_model={}", soldat_model)
    soldat_dto: Final = service.create(soldat=soldat_model.to_soldat())
    logger.debug("soldat_dto={}", soldat_dto)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{soldat_dto.id}"},
    )


@soldat_write_router.put(
    "/{soldat_id}"
)
def put(
    soldat_id: int,
    soldat_update_model: SoldatUpdateModel,
    request: Request,
    service: Annotated[SoldatWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um einen Soldaten zu aktualisieren.

    :param soldat_id: ID des zu aktualisierenden Soldaten als Pfadparameter
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit If-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    :raises ValidationError: Falls es bei Pydantic Validierungsfehler gibt
    :raises NotFoundError: Falls zur id kein Soldat existiert
    :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
    """
    if_match_value: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "soldat_id={}, if_match={}, soldat_update_model={}",
        soldat_id,
        if_match_value,
        soldat_update_model,
    )

    if if_match_value is None:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        )

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    soldat: Final = soldat_update_model.to_soldat()
    soldat_modified: Final = service.update(
        soldat=soldat,
        soldat_id=soldat_id,
        version=version_int,
    )
    logger.debug("soldat_modified={}", soldat_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{soldat_modified.version}"'},
    )
