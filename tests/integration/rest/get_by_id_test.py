# ruff: noqa: S101, D103
"""Tests für GET mit Pfadparameter für die ID."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


# in pyproject.toml bei der Table [tool.pytest.ini_options] gibt es das Array "markers"
@mark.rest
@mark.get_request
@mark.parametrize("soldat_id", [30, 1, 20])
def test_get_by_id_admin(soldat_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{soldat_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == soldat_id


@mark.rest
@mark.get_request
@mark.parametrize("soldat_id", [0, 999999])
def test_get_by_id_not_found(soldat_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{soldat_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_by_id_soldat() -> None:
    # arrange
    soldat_id: Final = 20
    token: Final = login(username="erenj")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{soldat_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    soldat_id_response: Final = response_body.get("id")
    assert soldat_id_response is not None
    assert soldat_id_response == soldat_id


@mark.rest
@mark.get_request
@mark.parametrize("soldat_id", [1, 30])
def test_get_by_id_not_allowed(soldat_id: int) -> None:
    # arrange
    token: Final = login(username="erenj")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{soldat_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.FORBIDDEN


@mark.rest
@mark.get_request
@mark.parametrize("soldat_id", [0, 999999])
def test_get_by_id_not_allowed_not_found(soldat_id: int) -> None:
    # arrange
    token: Final = login(username="alice")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{soldat_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.FORBIDDEN


@mark.rest
@mark.get_request
@mark.parametrize("soldat_id", [30, 1, 20])
def test_get_by_id_ungueltiger_token(soldat_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}XXX"}

    # act
    response: Final = get(
        f"{rest_url}/{soldat_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.get_request
@mark.parametrize("soldat_id", [30, 1, 20])
def test_get_by_id_ohne_token(soldat_id: int) -> None:
    # act
    response: Final = get(f"{rest_url}/{soldat_id}", verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.get_request
@mark.parametrize("soldat_id,if_none_match", [(20, '"0"'), (30, '"0"')])
def test_get_by_id_etag(soldat_id: int, if_none_match: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-None-Match": if_none_match,
    }

    # act
    response: Final = get(
        f"{rest_url}/{soldat_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_MODIFIED
    assert not response.text


@mark.rest
@mark.get_request
@mark.parametrize("soldat_id,if_none_match", [(30, 'xxx"'), (1, "xxx"), (20, "xxx")])
def test_get_by_id_etag_invalid(soldat_id: int, if_none_match: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-None-Match": if_none_match,
    }

    # act
    response: Final = get(
        f"{rest_url}/{soldat_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == soldat_id
