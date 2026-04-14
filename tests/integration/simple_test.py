# ruff: noqa: S101, D103
"""Einfache Tests mit pytest (siehe https://awesome-python.com/#testing)."""

from pytest import mark


@mark.simple
def test_simple() -> None:
    # pylint: disable-next=comparison-of-constants, comparison-with-itself
    assert True  # NOSONAR
