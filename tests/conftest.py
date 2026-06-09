from __future__ import annotations

import os

import pytest

import helo


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests against the live Helo API",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip ``@pytest.mark.integration`` tests unless ``--integration`` is passed."""
    if config.getoption("--integration"):
        return
    skip = pytest.mark.skip(reason="live API test; pass --integration to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)


LIVE_BASE_URL = os.environ.get("HELO_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def live_client() -> helo.Helo:
    """A client pointed at a live API, configured from the environment.

    Defaults to a local instance at ``http://localhost:8000``; override with
    ``HELO_BASE_URL``. Skips the test if ``HELO_API_KEY`` is not set so the suite
    stays runnable without credentials.
    """
    api_key = os.environ.get("HELO_API_KEY")
    if not api_key:
        pytest.skip("HELO_API_KEY not set")
    with helo.Helo(api_key=api_key, base_url=LIVE_BASE_URL) as client:
        yield client
