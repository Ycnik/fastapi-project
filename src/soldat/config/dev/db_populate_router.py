"""DbPopulateController."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from loguru import logger

from soldat.config.dev.db_populate import DbPopulateService, get_db_populate_service

__all__ = ["router"]


router: Final = APIRouter()


# "Dependency Injection" durch Depends
@router.post(
    "/db_populate",
    tags=["Admin"],
)
def populate(
    service: Annotated[DbPopulateService, Depends(get_db_populate_service)],
) -> JSONResponse:
    """Die DB mit Testdaten durch einen POST-Request neu zu laden.

    :return: JSON-Datensatz mit der Erfolgsmeldung
    :rtype: dict[str, str]
    """
    logger.warning(
        'REST-Schnittstelle zum Neuladen der DB aufgerufen von "{}"',
    )
    service.populate()
    return JSONResponse(content={"db_populate": "success"})
