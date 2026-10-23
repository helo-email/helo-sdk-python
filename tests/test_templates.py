from __future__ import annotations

from pytest_httpx import HTTPXMock

import sdk_helo_email as helo


def test_list(
    client: helo.Helo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1,
            "results": [{
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "updatedAt": "2024-01-01T00:00:00Z",
                    "name": "example",
                    "subject": "example",
                }],
        },
    )

    client.templates.list(
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/templates"


def test_create(
    client: helo.Helo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        method="POST",
        json={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z",
            "version": 1,
            "name": "example",
            "subject": "example",
        },
    )

    client.templates.create(
        name="test-name",
        subject="test-subject",
        html="test-html",
        mjml="test-mjml",
        text="test-text",
        channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/templates"


def test_render_draft(
    client: helo.Helo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        method="POST",
        json={"subject": "example"},
    )

    client.templates.render_draft(
        subject="test-subject",
        html="test-html",
        mjml="test-mjml",
        text="test-text",
        inline_styles=True,
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/templates/render"


def test_retrieve(
    client: helo.Helo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        method="GET",
        json={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z",
            "version": 1,
            "name": "example",
            "subject": "example",
        },
    )

    client.templates.retrieve(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/templates/550e8400-e29b-41d4-a716-446655440000"


def test_update(
    client: helo.Helo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        method="PATCH",
        json={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z",
            "version": 1,
            "name": "example",
            "subject": "example",
        },
    )

    client.templates.update(
        "550e8400-e29b-41d4-a716-446655440000",
        name="test-name",
        subject="test-subject",
        html="test-html",
        mjml="test-mjml",
        text="test-text",
        channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
        version=10,
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "PATCH"
    assert request.url.path == "/templates/550e8400-e29b-41d4-a716-446655440000"


def test_delete(
    client: helo.Helo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        method="DELETE",
        status_code=204,
    )

    client.templates.delete(
        "550e8400-e29b-41d4-a716-446655440000",
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "DELETE"
    assert request.url.path == "/templates/550e8400-e29b-41d4-a716-446655440000"


def test_render(
    client: helo.Helo, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        method="POST",
        json={"subject": "example"},
    )

    client.templates.render(
        "550e8400-e29b-41d4-a716-446655440000",
        inline_styles=True,
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/templates/550e8400-e29b-41d4-a716-446655440000/render"


async def test_list_async(
    async_client: helo.AsyncHelo, httpx_mock: HTTPXMock
) -> None:
    """The async resource is generated from the same operation, so one call proves the pair."""
    httpx_mock.add_response(
        method="GET",
        json={
            "totalCount": 1,
            "results": [{
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "updatedAt": "2024-01-01T00:00:00Z",
                    "name": "example",
                    "subject": "example",
                }],
        },
    )

    await async_client.templates.list(
    )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/templates"
