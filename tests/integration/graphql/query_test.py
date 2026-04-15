# ruff: noqa: S101, D103
"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login_graphql
from httpx import post
from pytest import mark

GRAPHQL_PATH: Final = "/graphql"


@mark.graphql
@mark.query
def test_query_id() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                soldat(soldatId: "20") {
                    nachname
                    geburtsdatum
                    geschlecht
                    rang
                    username
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    data: Final = response_body["data"]
    assert data is not None
    soldat: Final = data["soldat"]
    assert isinstance(soldat, dict)
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_id_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                soldat(soldatId: "999999") {
                    nachname
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"]["soldat"] is None
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_nachname() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                soldaten(suchparameter: {nachname: "Braun"}) {
                    id
                    version
                    nachname
                    geburtsdatum
                    geschlecht
                    rang
                    username
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    soldaten: Final = response_body["data"]["soldaten"]
    assert isinstance(soldaten, list)
    assert len(soldaten) > 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_nachname_notfound() -> None:
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                soldaten(suchparameter: {nachname: "Nichtvorhanden"}) {
                    id
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    soldaten: Final = response_body["data"]["soldaten"]
    assert isinstance(soldaten, list)
    assert len(soldaten) == 0
