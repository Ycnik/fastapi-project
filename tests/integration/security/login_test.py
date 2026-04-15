# ruff: noqa: S101, D103
"""Tests für Login."""

from http import HTTPStatus
from logging import getLogger
from typing import Final

from common_test import (
    base_url,
    ctx,
    login,
    timeout,
    token_path,
    username_admin,
)
from httpx import post
from pytest import mark

# fuer hypercorn: INFO statt DEBUG
getLogger("hpack.hpack").setLevel(level="INFO")
getLogger("hpack.table").setLevel(level="INFO")


@mark.login
def test_login_admin() -> None:
    # act
    token: Final = login()

    # then
    assert isinstance(token, str)
    assert token


@mark.login
def test_login_falsches_passwort() -> None:
    # arrange
    login_data: Final = {"username": username_admin, "password": "FALSCHES_PASSWORT"}

    # act
    response: Final = post(
        f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )

    # then
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.login
def test_login_ohne_daten() -> None:
    # arrange
    login_data: dict[str, str] = {}

    # act
    response: Final = post(
        f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )

    # then
    assert response.status_code == HTTPStatus.UNAUTHORIZED
