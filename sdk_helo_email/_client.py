from __future__ import annotations

import os
from typing import Any

from ._http import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    AsyncHttpClient,
    HttpClient,
)
from .resources import (
    ActivityResource,
    AsyncActivityResource,
    AsyncBroadcastsResource,
    AsyncChannelsResource,
    AsyncDomainsResource,
    AsyncSendingResource,
    AsyncStatisticsResource,
    AsyncSuppressionsResource,
    AsyncWebhooksResource,
    BroadcastsResource,
    ChannelsResource,
    DomainsResource,
    SendingResource,
    StatisticsResource,
    SuppressionsResource,
    WebhooksResource,
)


def _resolve_api_key(api_key: str | None) -> str:
    resolved = api_key or os.environ.get("HELO_API_KEY")
    if not resolved:
        raise ValueError(
            "No API key provided. Pass api_key= or set the HELO_API_KEY environment variable."
        )
    return resolved


class Helo:
    """Synchronous client for the Helo API."""

    activity: ActivityResource
    broadcasts: BroadcastsResource
    channels: ChannelsResource
    domains: DomainsResource
    sending: SendingResource
    statistics: StatisticsResource
    suppressions: SuppressionsResource
    webhooks: WebhooksResource

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._http = HttpClient(
            api_key=_resolve_api_key(api_key),
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.activity = ActivityResource(self._http)
        self.broadcasts = BroadcastsResource(self._http)
        self.channels = ChannelsResource(self._http)
        self.domains = DomainsResource(self._http)
        self.sending = SendingResource(self._http)
        self.statistics = StatisticsResource(self._http)
        self.suppressions = SuppressionsResource(self._http)
        self.webhooks = WebhooksResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Helo:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncHelo:
    """Asynchronous client for the Helo API."""

    activity: AsyncActivityResource
    broadcasts: AsyncBroadcastsResource
    channels: AsyncChannelsResource
    domains: AsyncDomainsResource
    sending: AsyncSendingResource
    statistics: AsyncStatisticsResource
    suppressions: AsyncSuppressionsResource
    webhooks: AsyncWebhooksResource

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._http = AsyncHttpClient(
            api_key=_resolve_api_key(api_key),
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.activity = AsyncActivityResource(self._http)
        self.broadcasts = AsyncBroadcastsResource(self._http)
        self.channels = AsyncChannelsResource(self._http)
        self.domains = AsyncDomainsResource(self._http)
        self.sending = AsyncSendingResource(self._http)
        self.statistics = AsyncStatisticsResource(self._http)
        self.suppressions = AsyncSuppressionsResource(self._http)
        self.webhooks = AsyncWebhooksResource(self._http)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncHelo:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
