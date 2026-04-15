# ruff: noqa: S101, D103
"""Tests für Mutations mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url
from httpx import post
from pytest import mark


@mark.graphql
@mark.mutation
def test_create() -> None:
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    soldatInput: {
                    vorname: "Vornamegraphql"
                    nachname: "Nachnamegraphql"
                    geburtsdatum: "2022-02-02"
                    geschlecht: WEIBLICH
                    rang: SOLDAT
                    ausruestung: {
                        waffe: Klinge
                        seriennummer: "AOT-Be1234"
                    }
                    verletzungen: [{
                        verletzungsbezeichnung: "Knochenbruch"
                        verletzungsdatum: "2024-03-11"
                        schweregrad: MITTEL
                        behandelt: true
                    }]
                    username: "testgraphql"
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response is not None
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert isinstance(response_body["data"]["create"]["id"], int)
    assert response_body.get("errors") is None


@mark.graphql
@mark.mutation
def test_create_invalid() -> None:
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    soldatInput: {
                    vorname: "falscher_Vorname"
                    nachname: "Nachnamegraphql_Falsch"
                    geburtsdatum: "2022-02-02"
                    geschlecht: WEIBLICH
                    rang: SOLDATfalsch
                    ausruestung: {
                        waffe: Klinge
                        seriennummer: "AOT-Be1234"
                    }
                    verletzungen: [{
                        verletzungsbezeichnung: "Knochenbruch"
                        verletzungsdatum: "2024-03-11"
                        schweregrad: MITTEL
                        behandelt: true
                    }]
                    username: "testgraphql"
                    }
                ) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"] is None
    errors: Final = response_body["errors"]
    assert isinstance(errors, list)
    assert len(errors) == 1
