"""MainApp."""

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Final

from fastapi.middleware.gzip import (
    GZipMiddleware,  # https://fastapi.tiangolo.com/advanced/middleware/#gzipmiddleware
)
from loguru import logger

from soldat.config import (
    dev_db_populate,
)
from soldat.config.dev.db_populate import db_populate
from soldat.repository.session_factory import engine
from soldat.router import (
    soldat_router,
    soldat_write_router,

)

from soldat.problem_details import create_problem_details

from fastapi import FastAPI, Request, Response, status

from soldat.service import (
    NotFoundError,
    VersionOutdatedError,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


TEXT_PLAIN: Final = "text/plain"


# --------------------------------------------------------------------------------------
# S t a r t u p   u n d   S h u t d o w n
# --------------------------------------------------------------------------------------
# https://fastapi.tiangolo.com/advanced/events
# pylint: disable=redefined-outer-name
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001, RUF029
    """DB und Keycloak neu laden, falls im dev-Modus, sowie Banner in der Konsole."""
    if dev_db_populate:
        logger.warning("Datenbank wird neu geladen")
        db_populate()
    yield
    logger.info("Der Server wird heruntergefahren")
    logger.info("Connection-Pool fuer die DB wird getrennt.")
    engine.dispose()


app: Final = FastAPI(lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=500)  # ty:ignore[invalid-argument-type]


# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(soldat_router, prefix="/rest")
app.include_router(soldat_write_router, prefix="/rest")



@app.get("/")
def read_root() -> dict[str, str]:
    """Liefert eine einfache Hello-World-Antwort."""
    return {"message": "Hello World"}

# --------------------------------------------------------------------------------------
# E x c e p t i o n   H a n d l e r
# --------------------------------------------------------------------------------------

@app.exception_handler(NotFoundError)
def not_found_error_handler(_request: Request, _err: NotFoundError) -> Response:
    """Errorhandler für NotFoundError.

    :param _err: NotFoundError aus der Geschäftslogik
    :return: Response mit Statuscode 404
    :rtype: Response
    """
    return create_problem_details(status_code=status.HTTP_404_NOT_FOUND)

@app.exception_handler(VersionOutdatedError)
def version_outdated_error_handler(
    _request: Request,
    err: VersionOutdatedError,
) -> Response:
    """Exception-Handling für VersionOutdatedError.

    :param _err: Exception, falls die Versionsnummer zum Aktualisieren veraltet ist
    :return: Response mit Statuscode 412
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail=str(err),
    )
