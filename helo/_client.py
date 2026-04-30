from __future__ import annotations

from typing import Any, Optional

from ._http import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, HttpClient
from .resources.activity import ActivityResource
from .resources.broadcasts import BroadcastsResource
from .resources.channels import ChannelsResource
from .resources.domains import DomainsResource
from .resources.sending import SendingResource
from .resources.statistics import StatisticsResource
from .resources.suppressions import SuppressionsResource
from .resources.webhook_endpoints import WebhookEndpointsResource


class Helo:
    """Python client for the Helo API.

    Usage::

        import helo

        client = helo.Helo(api_key="your-api-key")
        channel = client.channels.create(name="my-channel", delivery_type=helo.DeliveryType.LIVE)
    """

    activity: ActivityResource
    broadcasts: BroadcastsResource
    channels: ChannelsResource
    domains: DomainsResource
    sending: SendingResource
    statistics: StatisticsResource
    suppressions: SuppressionsResource
    webhook_endpoints: WebhookEndpointsResource

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._http = HttpClient(api_key=api_key, base_url=base_url, timeout=timeout)
        self.activity = ActivityResource(self._http)
        self.broadcasts = BroadcastsResource(self._http)
        self.channels = ChannelsResource(self._http)
        self.domains = DomainsResource(self._http)
        self.sending = SendingResource(self._http)
        self.statistics = StatisticsResource(self._http)
        self.suppressions = SuppressionsResource(self._http)
        self.webhook_endpoints = WebhookEndpointsResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "Helo":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
