"""DbPopulateController."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from loguru import logger

from soldat.config.dev.keycloak_populate import (
    KeycloakPopulateService,
    get_keycloak_populate_service,
)
from soldat.security import Role, RolesRequired, User

__all__ = ["router"]


router: Final = APIRouter()


# "Dependency Injection" durch Depends
@router.post(
    "/keycloak_populate",
    tags=["Admin"],
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def populate(
    request: Request,
    service: Annotated[KeycloakPopulateService, Depends(get_keycloak_populate_service)],
) -> JSONResponse:
    """Keycloak mit Testdaten durch einen POST-Request neu zu laden.

    :return: JSON-Datensatz mit der Erfolgsmeldung
    :rtype: dict[str, str]
    """
    current_user: Final[User] = request.state.current_user
    logger.warning(
        'REST-Schnittstelle zum Neuladen von Keycloak aufgerufen von "{}"',
        current_user.username,
    )
    service.populate()
    return JSONResponse(content={"keycloak_populate": "success"})
