from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from ..types.statistics import (
    StatisticsDailyResponse,
    StatisticsHourlyResponse,
    StatisticsTotalsResponse,
)
from ._base import AsyncBaseResource, BaseResource


def _range_params(
    from_: str,
    to: str,
    channel_id: str | None,
    tags: Sequence[str] | None,
    timezone: str | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {"from": from_, "to": to}
    if timezone is not None:
        params["timezone"] = timezone
    if channel_id is not None:
        params["channelId"] = channel_id
    if tags is not None:
        params["tags"] = tags
    return params


class StatisticsResource(BaseResource):
    def retrieve_hourly(
        self,
        *,
        from_: str,
        to: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsHourlyResponse:
        params = _range_params(from_, to, channel_id, tags)
        data = self._http.get("/activity/statistics/hourly", params=params)
        return StatisticsHourlyResponse.model_validate(data)

    def retrieve_daily(
        self,
        *,
        from_: str,
        to: str,
        timezone: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsDailyResponse:
        params = _range_params(from_, to, channel_id, tags, timezone=timezone)
        data = self._http.get("/activity/statistics/daily", params=params)
        return StatisticsDailyResponse.model_validate(data)

    def retrieve_totals(
        self,
        *,
        from_: str,
        to: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsTotalsResponse:
        params = _range_params(from_, to, channel_id, tags)
        data = self._http.get("/activity/statistics/totals", params=params)
        return StatisticsTotalsResponse.model_validate(data)


class AsyncStatisticsResource(AsyncBaseResource):
    async def retrieve_hourly(
        self,
        *,
        from_: str,
        to: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsHourlyResponse:
        params = _range_params(from_, to, channel_id, tags)
        data = await self._http.get("/activity/statistics/hourly", params=params)
        return StatisticsHourlyResponse.model_validate(data)

    async def retrieve_daily(
        self,
        *,
        from_: str,
        to: str,
        timezone: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsDailyResponse:
        params = _range_params(from_, to, channel_id, tags, timezone=timezone)
        data = await self._http.get("/activity/statistics/daily", params=params)
        return StatisticsDailyResponse.model_validate(data)

    async def retrieve_totals(
        self,
        *,
        from_: str,
        to: str,
        channel_id: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> StatisticsTotalsResponse:
        params = _range_params(from_, to, channel_id, tags)
        data = await self._http.get("/activity/statistics/totals", params=params)
        return StatisticsTotalsResponse.model_validate(data)
