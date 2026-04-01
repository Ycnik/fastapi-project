"""MainApp."""

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Final

from fastapi import FastAPI
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
async def lifespan() -> AsyncGenerator[None]:  # noqa: RUF029
    """DB und Keycloak neu laden, falls im dev-Modus, sowie Banner in der Konsole."""
    if dev_db_populate:
        logger.warning("Datenbank wird neu geladen")
        db_populate()
    yield
    logger.info("Der Server wird heruntergefahren")
    logger.info("Connection-Pool fuer die DB wird getrennt.")
    engine.dispose()


app: Final = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=500)  # ty:ignore[invalid-argument-type]


# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(soldat_router, prefix="/rest")


@app.get("/")
def read_root() -> dict[str, str]:
    """Liefert eine einfache Hello-World-Antwort."""
    return {"message": "Hello World"}
