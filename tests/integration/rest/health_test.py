# ruff: noqa: S101, D103
"""Tests für GET mit QUery-Parameter."""

from http import HTTPStatus
from typing import Any, Final

from common_test import ctx, health_url
from httpx import get
from pytest import mark


@mark.rest
@mark.health
def test_liveness() -> None:
    # act
    response: Final = get(f"{health_url}/liveness", verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    status: Final[Any | None] = response_body.get("status")
    assert status == "up"


@mark.rest
@mark.health
def test_readiness() -> None:
    # act
    response: Final = get(f"{health_url}/readiness", verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    status: Final[Any | None] = response_body.get("db")
    assert status == "up"
