"""REST-Schnittstelle für Login."""

from json import JSONDecodeError
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from soldat.security.dependencies import get_token_service
from soldat.security.login_data import LoginData
from soldat.security.token_service import TokenService

__all__ = ["router"]


router: Final = APIRouter(tags=["Login"])


async def request_body_to_dict(request: Request) -> dict[str, Any]:
    """Pydantic nicht verwenden: 401 statt Validierungsfehler 422."""
    try:
        body: dict[str, Any] = await request.json()
        return body
    except JSONDecodeError:
        # auch leerer Body
        return {}


@router.post("/token")
def token(
    body: Annotated[dict[str, Any], Depends(request_body_to_dict)],
    service: Annotated[TokenService, Depends(get_token_service)],
) -> Response:
    """Benutzername und Passwort per POST-Request, um einen JWT zu erhalten.

    - **body**: Request-Body als dict durch request.json() oder {} im Fehlerfall
    """
    logger.debug("body={}", body)
    try:
        # Dictionary Unpacking
        # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
        login_data: Final = LoginData(**body)
    except TypeError:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    token: Final = service.token(
        username=login_data.username,
        password=login_data.password,
    )
    access_token: Final = token["access_token"]
    roles: Final = service.get_roles_from_token(token=access_token)

    response_body: Final = {
        "token": access_token,
        "expires_in": token["expires_in"],
        "rollen": roles,
    }
    logger.debug("response body={}", response_body)
    return JSONResponse(content=response_body)
