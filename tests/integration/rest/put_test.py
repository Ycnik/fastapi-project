# ruff: noqa: S101, D103
"""Tests für PUT."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import put
from pytest import mark

EMAIL_UPDATE: Final = "alice@acme.de.put"
HOMEPAGE_UPDATE: Final = "https://www.acme.ch.put"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    soldat_id: Final = 40
    if_match: Final = '"0"'
    geaenderter_soldat: Final = {
        "vorname": "Erwingeaendert",
        "nachname": "Smithgeaendert",
        "rang": "KOMMANDANT",
        "geburtsdatum": "1985-10-14",
        "geschlecht": "M",
        "username": "erwins",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{soldat_id}",
        json=geaenderter_soldat,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text


@mark.rest
@mark.put_request
def test_put_invalid() -> None:
    # arrange
    soldat_id: Final = 40
    geaenderter_soldat_invalid: Final = {
        "vorname": "ErwinGeaendert_Falsch",
        "nachname": "SmithGeaendert_falsch",
        "rang": "keinrang",
        "geburtsdatum": "1985-10-14",
        "geschlecht": "M",
        "username": "erwins",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "If-Match": '"0"',
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{soldat_id}",
        json=geaenderter_soldat_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "nachname" in response.text


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    soldat_id: Final = 999999
    if_match: Final = '"0"'
    geaenderter_soldat: Final = {
        "vorname": "Erwin",
        "nachname": "Smith",
        "rang": "KOMMANDANT",
        "geburtsdatum": "1985-10-14",
        "geschlecht": "M",
        "username": "erwins",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{soldat_id}",
        json=geaenderter_soldat,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_ohne_versionsnr() -> None:
    # arrange
    soldat_id: Final = 40
    geaenderter_soldat: Final = {
        "vorname": "Erwin",
        "nachname": "Smith",
        "rang": "KOMMANDANT",
        "geburtsdatum": "1985-10-14",
        "geschlecht": "M",
        "username": "erwins",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{soldat_id}",
        json=geaenderter_soldat,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_REQUIRED


@mark.rest
@mark.put_request
def test_put_alte_versionsnr() -> None:
    # arrange
    soldat_id: Final = 40
    if_match: Final = '"-1"'
    geaenderter_soldat: Final = {
        "vorname": "Erwin",
        "nachname": "Smith",
        "rang": "KOMMANDANT",
        "geburtsdatum": "1985-10-14",
        "geschlecht": "M",
        "username": "erwins",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{soldat_id}",
        json=geaenderter_soldat,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED


@mark.rest
@mark.put_request
def test_put_ungueltige_versionsnr() -> None:
    # arrange
    soldat_id: Final = 40
    if_match: Final = '"xy"'
    geaenderter_soldat: Final = {
        "vorname": "Erwin",
        "nachname": "Smith",
        "rang": "KOMMANDANT",
        "geburtsdatum": "1985-10-14",
        "geschlecht": "M",
        "username": "erwins",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{soldat_id}",
        json=geaenderter_soldat,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
    assert not response.text


@mark.rest
@mark.put_request
def test_put_versionsnr_ohne_quotes() -> None:
    # arrange
    soldat_id: Final = 40
    if_match: Final = "0"
    geaenderter_soldat: Final = {
        "vorname": "Erwin",
        "nachname": "Smith",
        "rang": "KOMMANDANT",
        "geburtsdatum": "1985-10-14",
        "geschlecht": "M",
        "username": "erwins",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{soldat_id}",
        json=geaenderter_soldat,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
