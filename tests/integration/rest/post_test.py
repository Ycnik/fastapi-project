# ruff: noqa: S101, D103
"""Tests für POST."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, rest_url
from httpx import post
from pytest import mark

token: str | None


@mark.rest
@mark.post_request
def test_post() -> None:
    # arrange
    neuer_soldat: Final = {
        "vorname": "Erwintest",
        "nachname": "Smithtest",
        "rang": "KOMMANDANT",
        "geburtsdatum": "1985-10-14",
        "geschlecht": "M",
        "ausruestung": {"waffe": "Klinge", "seriennummer": "AOT-220205"},
        "verletzungen": [
            {
                "verletzungsbezeichnung": "Armverletzung",
                "schweregrad": "SCHWER",
                "behandelt": False,
                "verletzungsdatum": "2022-02-01",
            }
        ],
        "username": "erwins",
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_soldat,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neuer_soldat_invalid: Final = {
        "vorname": "vorname_falsch",
        "nachname": "Nachnamerest",
        "geburtsdatum": "2022-02-01",
        "geschlecht": "W",
        "rang": "SOLDAT",
        "ausruestung": {"waffe": "Klinge", "serienummer": "543"},
        "verletzungen": [
            {
                "verletzungsbezeichnung": "Knochenbruch",
                "behandelt": "false",
                "schweregrad": "LEICHT",
                "verletzungsdatum": "2022-02-01",
            }
        ],  # noqa: E501
        "username": "testrestinvalid",
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_soldat_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@mark.rest
@mark.post_request
def test_post_invalid_json() -> None:
    # arrange
    json_invalid: Final = '{"nachname" "Nachname"}'
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=json_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "should be a valid dictionary" in response.text
